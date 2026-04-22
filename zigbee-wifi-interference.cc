#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/lr-wpan-module.h"
#include "ns3/wifi-module.h"
#include "ns3/mobility-module.h"
#include "ns3/internet-module.h"
#include "ns3/applications-module.h"
#include "ns3/flow-monitor-module.h"

using namespace ns3;
using namespace ns3::lrwpan;

// -------- GLOBAL VARIABLES --------
bool wifiActive = false;
bool channelSwitched = false;

Time detectionTime;
Time switchTime;

// -------- SWITCH CHANNEL --------
void SwitchChannel (Ptr<LrWpanNetDevice> dev)
{
    // Add delay to simulate realistic switching latency
    Simulator::Schedule (MilliSeconds (100), [dev]() {

        switchTime = Simulator::Now ();

        std::cout << "Channel switched at: "
                  << switchTime.GetSeconds () << "s\n";

        Ptr<PhyPibAttributes> pibAttr = Create<PhyPibAttributes> ();
        pibAttr->phyCurrentChannel = 15;

        dev->GetPhy ()->PlmeSetAttributeRequest (phyCurrentChannel, pibAttr);
    });
}

// -------- INTERFERENCE CHECK --------
void CheckInterference (Ptr<LrWpanNetDevice> dev)
{
    if (wifiActive && !channelSwitched)
    {
        double ed = 1.0; // simulated ED

        if (ed > 0.5)
        {
            detectionTime = Simulator::Now ();

            std::cout << "Interference detected at: "
                      << detectionTime.GetSeconds () << "s\n";

            SwitchChannel (dev);
            channelSwitched = true;  // prevent repeated switching
        }
    }

    Simulator::Schedule (Seconds (1.0),
                         &CheckInterference, dev);
}

// -------- START WIFI --------
void StartWifi ()
{
    wifiActive = true;

    std::cout << "WiFi started at: "
              << Simulator::Now ().GetSeconds () << "s\n";
}

// -------- THROUGHPUT LOG --------
void LogThroughput (Ptr<FlowMonitor> monitor,
                    Ptr<OutputStreamWrapper> stream)
{
    monitor->CheckForLostPackets ();
    auto stats = monitor->GetFlowStats ();

    double throughput = 0;

    for (auto &flow : stats)
    {
        if (flow.second.timeLastRxPacket.GetSeconds () > 0)
        {
            throughput += flow.second.rxBytes * 8.0 /
                          (flow.second.timeLastRxPacket.GetSeconds () -
                           flow.second.timeFirstTxPacket.GetSeconds ()) / 1000;
        }
    }

    *stream->GetStream () << Simulator::Now ().GetSeconds ()
                          << " " << throughput << std::endl;

    Simulator::Schedule (Seconds (1.0),
                         &LogThroughput, monitor, stream);
}

// -------- MAIN --------
int main ()
{
    // -------- NODES --------
    NodeContainer zigbee;
    zigbee.Create (3);

    NodeContainer wifiSta;
    wifiSta.Create (2);

    NodeContainer wifiAp;
    wifiAp.Create (1);

    // -------- MOBILITY --------
    MobilityHelper mobility;
    mobility.SetMobilityModel ("ns3::ConstantPositionMobilityModel");

    mobility.Install (zigbee);
    mobility.Install (wifiSta);
    mobility.Install (wifiAp);

    // -------- ZIGBEE --------
    LrWpanHelper lr;
    NetDeviceContainer devs = lr.Install (zigbee);
    lr.CreateAssociatedPan (devs, 0);

    Ptr<LrWpanNetDevice> coord =
        DynamicCast<LrWpanNetDevice> (devs.Get (0));

    // -------- WIFI --------
    WifiHelper wifi;
    wifi.SetStandard (WIFI_STANDARD_80211g);

    YansWifiChannelHelper channel = YansWifiChannelHelper::Default ();
    YansWifiPhyHelper phy;
    phy.SetChannel (channel.Create ());

    WifiMacHelper mac;
    Ssid ssid = Ssid ("test");

    // STA
    mac.SetType ("ns3::StaWifiMac",
                 "Ssid", SsidValue (ssid));
    NetDeviceContainer staDevices =
        wifi.Install (phy, mac, wifiSta);

    // AP
    mac.SetType ("ns3::ApWifiMac",
                 "Ssid", SsidValue (ssid));
    NetDeviceContainer apDevice =
        wifi.Install (phy, mac, wifiAp);

    // -------- INTERNET --------
    InternetStackHelper stack;
    stack.Install (wifiSta);
    stack.Install (wifiAp);

    Ipv4AddressHelper address;
    address.SetBase ("10.1.1.0", "255.255.255.0");

    Ipv4InterfaceContainer staInterfaces =
        address.Assign (staDevices);
    address.Assign (apDevice);

    // -------- TRAFFIC --------
    uint16_t port = 9;

    // Receiver (IMPORTANT)
    PacketSinkHelper sink ("ns3::UdpSocketFactory",
                           InetSocketAddress (Ipv4Address::GetAny (), port));

    ApplicationContainer sinkApp =
        sink.Install (wifiSta.Get (0));
    sinkApp.Start (Seconds (0.0));
    sinkApp.Stop (Seconds (25.0));

    // Sender
    OnOffHelper onoff ("ns3::UdpSocketFactory",
                       Address (InetSocketAddress (
                           staInterfaces.GetAddress (0), port)));

    onoff.SetConstantRate (DataRate ("5Mbps"));

    ApplicationContainer app =
        onoff.Install (wifiAp.Get (0));

    app.Start (Seconds (5.0));
    app.Stop (Seconds (20.0));

    // -------- FLOW MONITOR --------
    FlowMonitorHelper flowmon;
    Ptr<FlowMonitor> monitor = flowmon.InstallAll ();

    // -------- FILE OUTPUT --------
    AsciiTraceHelper ascii;
    Ptr<OutputStreamWrapper> stream =
        ascii.CreateFileStream ("throughput.tr");

    // -------- SCHEDULE --------
    Simulator::Schedule (Seconds (5.0), &StartWifi);
    Simulator::Schedule (Seconds (6.0),
                         &CheckInterference, coord);

    Simulator::Schedule (Seconds (1.0),
                         &LogThroughput, monitor, stream);

    Simulator::Stop (Seconds (25.0));
    Simulator::Run ();

    // -------- RESULTS --------
    std::cout << "\n===== RESULTS =====\n";
    std::cout << "Detection Time: "
              << detectionTime.GetSeconds () << " s\n";

    std::cout << "Switch Time: "
              << switchTime.GetSeconds () << " s\n";

    std::cout << "Switching Latency: "
              << (switchTime - detectionTime).GetSeconds ()
              << " s\n";

    Simulator::Destroy ();
    return 0;
}
