"""
Meridian Supply Co. knowledge base.
Each entry is a chunk: doc_id, section, category, and the text content.
These get embedded and stored in ChromaDB on startup.
"""

DOCUMENTS = [

    # ── ISA-2400 Industrial Sensor Array ────────────────────────────────────
    {
        "id": "isa-2400-overview",
        "doc": "ISA-2400 Industrial Sensor Array",
        "section": "Product Overview",
        "category": "Sensors",
        "text": (
            "The ISA-2400 Industrial Sensor Array is a multi-channel environmental monitoring unit designed "
            "for factory floors, warehouses, and outdoor industrial sites. It captures temperature, humidity, "
            "vibration, and ambient light simultaneously across up to 8 sensor inputs. The device operates "
            "on 24V DC or PoE and supports Modbus RTU, Modbus TCP, and MQTT output protocols. "
            "Operating range is -40°C to 85°C with an IP67 enclosure rating."
        ),
    },
    {
        "id": "isa-2400-install",
        "doc": "ISA-2400 Industrial Sensor Array",
        "section": "Installation & Wiring",
        "category": "Sensors",
        "text": (
            "Mount the ISA-2400 on a DIN rail or flat surface using the provided M5 hardware. "
            "Maintain at least 50mm clearance on all sides for airflow. "
            "Power input accepts 18–30V DC on terminals L+ and L–. For PoE installations, use an 802.3af-compliant "
            "switch — the unit draws a maximum of 12W. "
            "Sensor inputs use M12 4-pin connectors. Pin 1: +V, Pin 2: Signal, Pin 3: GND, Pin 4: Shield. "
            "All wiring should be run in conduit and separated from high-voltage lines by at least 150mm."
        ),
    },
    {
        "id": "isa-2400-config",
        "doc": "ISA-2400 Industrial Sensor Array",
        "section": "Configuration & Calibration",
        "category": "Sensors",
        "text": (
            "Access the web interface at 192.168.1.100 (default) after connecting via Ethernet. "
            "Default credentials: admin / meridian2400. Change these immediately on first login. "
            "Under Settings > Output, select your protocol (Modbus TCP or MQTT) and configure the broker address, "
            "port, and topic prefix. Calibration offsets for each channel can be set in Settings > Sensors. "
            "Factory calibration is performed at 25°C — apply an offset if your site baseline differs. "
            "Firmware updates are pushed via the web interface under System > Update."
        ),
    },
    {
        "id": "isa-2400-troubleshoot",
        "doc": "ISA-2400 Industrial Sensor Array",
        "section": "Troubleshooting",
        "category": "Sensors",
        "text": (
            "LED STATUS: Solid green = normal operation. Blinking amber = network not connected. "
            "Solid red = sensor fault on one or more channels — check the Faults tab in the web UI. "
            "If a channel reads –999, the sensor on that input is disconnected or wired incorrectly. "
            "For MQTT connection failures, verify the broker IP is reachable from the device subnet. "
            "Factory reset: hold the recessed RESET button for 10 seconds until the LED flashes red three times. "
            "Contact support@meridiansupply.com with the serial number and a copy of the System > Logs export."
        ),
    },

    # ── GCU-1800 Gateway Controller ─────────────────────────────────────────
    {
        "id": "gcu-1800-overview",
        "doc": "GCU-1800 Gateway Controller",
        "section": "Product Overview",
        "category": "Hardware",
        "text": (
            "The GCU-1800 is an edge gateway designed to aggregate data from up to 32 field devices "
            "and forward it to cloud or on-premise systems. It runs a hardened Linux OS (kernel 5.15) "
            "with 4GB RAM and 32GB eMMC storage. Connectivity options: 4x Gigabit Ethernet, 2x RS-485, "
            "1x RS-232, 2x USB-A 3.0, and an optional 4G LTE modem (GCU-1800-LTE variant). "
            "Supports OPC-UA, MQTT, REST, and Modbus TCP natively."
        ),
    },
    {
        "id": "gcu-1800-api",
        "doc": "GCU-1800 Gateway Controller",
        "section": "Local REST API",
        "category": "Hardware",
        "text": (
            "The GCU-1800 exposes a local REST API on port 8080. Authentication uses Bearer tokens "
            "generated at Settings > API Keys. "
            "GET /api/v1/devices — list all connected devices and their last-seen timestamp. "
            "GET /api/v1/devices/{id}/data — latest readings for a specific device. "
            "POST /api/v1/devices/{id}/command — send a command payload (JSON body). "
            "GET /api/v1/system/health — CPU, memory, disk, and uptime. "
            "All responses are JSON. Rate limit is 100 requests/minute per API key."
        ),
    },
    {
        "id": "gcu-1800-network",
        "doc": "GCU-1800 Gateway Controller",
        "section": "Network Configuration",
        "category": "Hardware",
        "text": (
            "ETH0 is the management interface, defaulting to DHCP. ETH1–ETH3 are for field devices. "
            "Assign static IPs via the web UI at Settings > Network, or via the CLI: "
            "`nmcli con mod eth0 ipv4.addresses 10.0.1.5/24 ipv4.gateway 10.0.1.1 ipv4.method manual`. "
            "VLAN tagging is supported on all interfaces. Use the Firewall tab to restrict management "
            "access to specific subnets — default allows all on ETH0. "
            "NTP sync is required for accurate timestamps; configure the NTP server under Settings > System."
        ),
    },

    # ── RP-3200 RFID Reader Pro ──────────────────────────────────────────────
    {
        "id": "rp-3200-overview",
        "doc": "RP-3200 RFID Reader Pro",
        "section": "Product Overview",
        "category": "Hardware",
        "text": (
            "The RP-3200 is a fixed UHF RFID reader supporting EPC Gen 2 / ISO 18000-6C. "
            "It supports up to 4 antenna ports (TNC connectors, 50Ω) with per-port power control from 10–33 dBm. "
            "Reads up to 1,000 tags/second in dense reader mode. "
            "Ethernet and USB connectivity. Outputs via LLRP 1.1, REST, or a native SDK available for Python, Java, and .NET. "
            "The RP-3200 is designed for dock doors, conveyor lines, and portal installations."
        ),
    },
    {
        "id": "rp-3200-antenna",
        "doc": "RP-3200 RFID Reader Pro",
        "section": "Antenna Setup & Read Range",
        "category": "Hardware",
        "text": (
            "For portal installations, use circular-polarized antennas (6 dBic gain recommended) mounted at "
            "1.2m height, facing inward. Maximum read range with a standard RAIN RFID label is 6–8m at 30 dBm. "
            "Reduce transmit power if you're getting false reads from adjacent aisles — start at 20 dBm and increase. "
            "Antenna cables: keep runs under 5m with LMR-400 to minimize loss. "
            "Use port multiplexing when more than 4 antennas are needed — Meridian offers the AM-8 antenna multiplexer "
            "as an accessory (sold separately, SKU: AM-8-50)."
        ),
    },
    {
        "id": "rp-3200-integration",
        "doc": "RP-3200 RFID Reader Pro",
        "section": "Integration Guide",
        "category": "Hardware",
        "text": (
            "Python SDK example: `from meridian_rfid import RP3200; reader = RP3200('192.168.1.200'); reader.start_inventory()`. "
            "Tag reads are emitted as events: `reader.on_tag_read = my_callback`. Each event contains EPC, RSSI, antenna port, and UTC timestamp. "
            "For Kafka integration, the reader can publish directly to a topic — configure under Settings > Output > Kafka. "
            "For MQTT, set the broker, port, and base topic at Settings > Output > MQTT. "
            "Avoid running inventory continuously for more than 8 hours without a 5-minute idle cycle to prevent RF module overheating."
        ),
    },

    # ── NS-24 Network Switch ─────────────────────────────────────────────────
    {
        "id": "ns-24-overview",
        "doc": "NS-24 Network Switch Configuration Guide",
        "section": "Overview",
        "category": "Networking",
        "text": (
            "The NS-24 is a managed 24-port Gigabit switch with 4 SFP uplinks and a full CLI. "
            "It supports 802.1Q VLANs, RSTP, LACP, QoS (802.1p and DSCP), SNMP v2c/v3, and port mirroring. "
            "Management access via web UI (port 443), SSH (port 22), or serial console (115200 8N1). "
            "Default management IP: 192.168.0.1. Default credentials: admin / admin — change on first login."
        ),
    },
    {
        "id": "ns-24-vlan",
        "doc": "NS-24 Network Switch Configuration Guide",
        "section": "VLAN Configuration",
        "category": "Networking",
        "text": (
            "Create a VLAN: `vlan database; vlan 10 name FIELD_DEVICES; exit`. "
            "Assign ports to a VLAN: `interface ge1/0/1; switchport mode access; switchport access vlan 10`. "
            "For trunk ports (carrying multiple VLANs): `switchport mode trunk; switchport trunk allowed vlan 10,20,30`. "
            "The management VLAN is 1 by default — move it to a dedicated VLAN in production deployments. "
            "Verify with: `show vlan brief`. VLAN config is saved with `write memory`."
        ),
    },
    {
        "id": "ns-24-qos",
        "doc": "NS-24 Network Switch Configuration Guide",
        "section": "QoS & PoE",
        "category": "Networking",
        "text": (
            "Ports 1–16 support PoE+ (802.3at, up to 30W per port). Total PoE budget is 370W. "
            "To prioritize RFID reader traffic: `qos map dscp-to-tc 46 to tc 6` (EF DSCP → high priority queue). "
            "For field device ports, trust DSCP: `interface ge1/0/1; qos trust dscp`. "
            "PoE scheduling: set a lower priority on non-critical devices under Settings > PoE so cameras "
            "or sensors don't starve out readers during a power event. "
            "Check PoE status per port: `show power inline`."
        ),
    },

    # ── Product Catalog ──────────────────────────────────────────────────────
    {
        "id": "catalog-sensors",
        "doc": "Meridian Supply Co. 2026 Product Catalog",
        "section": "Sensors & Monitoring",
        "category": "Catalog",
        "text": (
            "ISA-2400 Industrial Sensor Array — $2,499. Multi-channel environmental monitoring, 8 inputs, "
            "IP67, Modbus/MQTT. Lead time: 5–7 business days. "
            "DLM-900 Data Logger Module — $899. Standalone data logging, 16GB internal storage, USB export, "
            "4 analog inputs, RS-485. Lead time: 3–5 business days. "
            "Bulk pricing available for orders of 10+ units — contact your account manager for a quote."
        ),
    },
    {
        "id": "catalog-hardware",
        "doc": "Meridian Supply Co. 2026 Product Catalog",
        "section": "Hardware & Controllers",
        "category": "Catalog",
        "text": (
            "GCU-1800 Gateway Controller — $1,899. Edge gateway, 32 device capacity, 4G LTE variant available (+$350). "
            "RP-3200 RFID Reader Pro — $3,200. UHF Gen2, 4-port, up to 1,000 tags/sec. Lead time: 7–10 days. "
            "AM-8 Antenna Multiplexer — $420. Extends RP-3200 to 8 antenna ports. "
            "AUA-UHF Antenna (circular polarized, 6dBic) — $95 each. All hardware includes a 2-year warranty."
        ),
    },
    {
        "id": "catalog-networking",
        "doc": "Meridian Supply Co. 2026 Product Catalog",
        "section": "Networking",
        "category": "Catalog",
        "text": (
            "NS-24 Network Switch — $1,250. 24-port managed GbE, 4 SFP uplinks, 370W PoE budget, full CLI. "
            "PSU-48 Power Supply 48V — $349. DIN-rail mount, 48V/10A output, redundant input 100–240VAC. "
            "MHK-500 Mounting Hardware Kit — $125. Universal rack and DIN-rail hardware, includes all fasteners. "
            "Volume discounts: 5% off for 5+ units, 10% off for 20+ units of the same SKU."
        ),
    },
    {
        "id": "catalog-software-services",
        "doc": "Meridian Supply Co. 2026 Product Catalog",
        "section": "Software & Services",
        "category": "Catalog",
        "text": (
            "ISL-PRO Integration Software License — $4,500/seat. Includes REST API framework, Kafka connector, "
            "MQTT broker, and 1 year of updates. Multi-site license available. "
            "CSP-2000 Calibration Service Pack — $2,000. On-site calibration for up to 10 devices, "
            "includes calibration certificates and a 6-month accuracy guarantee. "
            "Annual support contracts available at 18% of hardware list price — includes remote diagnostics, "
            "firmware updates, and 4-hour response SLA."
        ),
    },

    # ── Support & Warranty ───────────────────────────────────────────────────
    {
        "id": "support-warranty",
        "doc": "Support & Warranty Policy",
        "section": "Warranty Terms",
        "category": "Support",
        "text": (
            "All Meridian hardware carries a 2-year limited warranty covering manufacturing defects. "
            "Warranty does not cover damage from incorrect installation, overvoltage, physical impact, or "
            "use outside the rated environmental spec. "
            "Software licenses include 1 year of updates; extended update agreements are available. "
            "To initiate a warranty claim, submit a ticket at support.meridiansupply.com with the serial number, "
            "proof of purchase, and a description of the fault. "
            "Approved warranty replacements ship within 3 business days."
        ),
    },
    {
        "id": "support-rma",
        "doc": "Support & Warranty Policy",
        "section": "RMA Process",
        "category": "Support",
        "text": (
            "RMA (Return Merchandise Authorization) is required before sending any unit back. "
            "Request an RMA number via the support portal or by emailing rma@meridiansupply.com. "
            "Ship the unit in its original packaging where possible — units damaged in transit due to inadequate "
            "packaging are not covered. Include the RMA number on the outside of the box. "
            "Standard evaluation turnaround is 10 business days. Expedited evaluation (3 days) is available "
            "for customers with an active support contract."
        ),
    },
    {
        "id": "support-sla",
        "doc": "Support & Warranty Policy",
        "section": "Support Tiers & SLA",
        "category": "Support",
        "text": (
            "Standard Support (included with all products): email support, 48-hour response, business hours. "
            "Professional Support ($X/year, 18% of hardware list): email + phone, 4-hour response, business hours, "
            "remote diagnostics, firmware access. "
            "Enterprise Support (custom pricing): 24/7 coverage, 1-hour response, dedicated account engineer, "
            "on-site support credits included. "
            "Support portal: support.meridiansupply.com. Direct line for Enterprise customers: +1 800-555-0190."
        ),
    },
]
