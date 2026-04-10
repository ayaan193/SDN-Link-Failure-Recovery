# SDN Link Failure Detection and Recovery using POX

## 📌 Problem Statement

Modern networks must remain operational even when links fail. Traditional networks rely on distributed protocols, which can be slow and complex.

This project demonstrates a **Software Defined Networking (SDN)** approach using the **POX controller** and **Mininet**, where the controller dynamically detects link failures and ensures continuous connectivity by adapting to topology changes.

---

## 🧠 Objective

* Detect link failures in a network topology
* Dynamically adapt forwarding behavior using an SDN controller
* Maintain communication between hosts despite failures
* Demonstrate controller–switch interaction using OpenFlow

---

## 🏗️ System Overview

* **Mininet** → Simulates network topology (hosts, switches, links)
* **POX Controller** → Acts as control plane (decision making)
* **OpenFlow** → Communication protocol between switches and controller

### Topology Used

```
h1 --- s1 --- s2 --- h2
        \       /
         \--- s3
```

* Primary path: `s1 → s2`
* Backup path: `s1 → s3 → s2`

---

## ⚙️ Setup & Execution Steps

### 1. Clone POX (if not already)

```bash
git clone https://github.com/noxrepo/pox.git
cd pox
```

---

### 2. Run POX Controller

```bash
./pox.py openflow.discovery link_failover
```

---

### 3. Run Mininet Topology

(Open a new terminal)

```bash
sudo mn --custom topo.py --topo mytopo --controller remote
```

---

### 4. Test Network Connectivity

```bash
pingall
```

---

### 5. Simulate Link Failure

```bash
link s1 s2 down
```

---

### 6. Verify Recovery

```bash
h1 ping h2
```

---

### 7. Restore Link

```bash
link s1 s2 up
```

---

## ✅ Expected Output

* Under normal conditions:

  * All hosts communicate successfully
  * `pingall` shows **0% packet loss**

* During link failure:

  * Controller detects failure
  * Traffic reroutes via alternate path
  * Connectivity is maintained

* After link restoration:

  * Network returns to normal operation

---

## 🎥 Working Demonstration

### ✔ Functional Correctness

* Controller successfully handles `PacketIn` events
* Flow rules are installed dynamically
* Network adapts to topology changes

### ✔ Live Demo Flow

1. Start controller
2. Start Mininet
3. Show `pingall` (normal)
4. Break link (`link s1 s2 down`)
5. Show communication still works
6. Restore link

---

## 🧪 Testing & Validation

### 🔹 Scenario 1: Normal Operation

* Command: `pingall`
* Result: 0% packet loss

---

### 🔹 Scenario 2: Link Failure

* Command: `link s1 s2 down`
* Result: Communication continues via alternate path

---

### 🔹 Scenario 3: Link Restoration

* Command: `link s1 s2 up`
* Result: Network returns to normal operation

---

## 📊 Performance Observation

### 🔹 Latency (Ping)

```bash
h1 ping h2
```

* Slight delay during failure
* Stabilizes quickly after rerouting

---

### 🔹 Throughput (iPerf)

```bash
iperf h1 h2
```

* Throughput remains stable before and after failure

---

### 🔹 Flow Table Inspection

```bash
dpctl dump-flows
```

* Shows dynamically installed flow rules

---

## 📸 Proof of Execution

Include screenshots of:

* `pingall` output
* Link failure (`link s1 s2 down`)
* Ping after failure
* POX controller logs
* Flow table (`dpctl dump-flows`)
* iPerf results

---

## 📂 Project Structure

```
SDN-Link-Failure-Recovery/
├── topo.py
├── pox/
│   └── ext/
│       └── link_failover.py
├── README.md
├── screenshots/
```

---

## ⚠️ Limitations

* Uses learning-switch behavior instead of explicit path computation
* Does not implement shortest path algorithms (e.g., Dijkstra)
* POX is not production-grade

---

## 🚀 Future Improvements

* Implement shortest path routing
* Add QoS-based routing
* Extend to larger topologies
* Use advanced controllers like Ryu or ONOS

---

## 📚 References

1. POX Controller Documentation – https://github.com/noxrepo/pox
2. Mininet Documentation – http://mininet.org
3. OpenFlow Specification – https://opennetworking.org
4. SDN Concepts – “Software Defined Networking: A Comprehensive Survey”

---

## 🏁 Conclusion

This project demonstrates how SDN enables dynamic network control. By separating control and data planes, the system can detect link failures and maintain connectivity through alternate paths, ensuring reliable network operation.
