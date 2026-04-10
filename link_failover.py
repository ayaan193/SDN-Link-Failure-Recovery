from pox.core import core
import pox.openflow.libopenflow_01 as of

from pox.lib.packet import ethernet
from pox.lib.packet import ipv4
from pox.lib.packet import udp

log = core.getLogger()

# Track path state
active_path = "primary"
last_state = None

# MAC learning table
mac_to_port = {}



def _handle_PacketIn(event):
    global active_path

    packet = event.parsed

    if not packet.parsed:
        return

    # Only allow ARP + IP
    if packet.type != 0x0806 and packet.type != 0x0800:
        return

    dpid = event.dpid
    in_port = event.port

    src = packet.src
    dst = packet.dst

    # Learn MAC
    mac_to_port[(dpid, src)] = in_port

    # Forward decision
    if (dpid, dst) in mac_to_port:
        out_port = mac_to_port[(dpid, dst)]
    else:
        out_port = of.OFPP_FLOOD

    # Install flow
    msg = of.ofp_flow_mod()
    msg.match.dl_src = src
    msg.match.dl_dst = dst
    msg.idle_timeout = 10
    msg.hard_timeout = 30
    msg.actions.append(of.ofp_action_output(port=out_port))
    event.connection.send(msg)

    # 🔥 CRITICAL: send packet immediately
    msg2 = of.ofp_packet_out()
    msg2.data = event.ofp
    msg2.actions.append(of.ofp_action_output(port=out_port))
    event.connection.send(msg2)

def _handle_LinkEvent(event):
    global active_path, last_state

    if event.removed and last_state != "down":
        log.info("⚠️ Link failure detected!")
        active_path = "backup"
        log.info("🔁 Switched to BACKUP path")
        last_state = "down"

    elif event.added and last_state != "up":
        log.info("✅ Link restored!")
        active_path = "primary"
        log.info("🔁 Switched to PRIMARY path")
        last_state = "up"


def launch():
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)

    # Required for link detection
    core.openflow_discovery.addListenerByName("LinkEvent", _handle_LinkEvent)

    log.info("🚀 Link Failover Controller Started")
