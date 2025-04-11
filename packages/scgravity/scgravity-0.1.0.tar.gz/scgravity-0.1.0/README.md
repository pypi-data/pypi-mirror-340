# scgravity

**scgravity** is a Python package for self-consistent flow decomposition based on the gravity model.  
It estimates latent *mass* values (`m_i^out`, `m_j^in`) and a *deterrence function* `Q(d)` from observed flows `f_ij` and pairwise distances `d_ij`.  
This approach is commonly used in spatial interaction modeling, such as international trade, transportation networks, and migration systems.

---

## 📘 Background: Gravity Model

The gravity model is a fundamental tool for modeling interactions between entities (e.g., countries, cities).  
It assumes that the observed flow `f_ij` between node *i* and *j* depends on their intrinsic properties and the distance between them, via:

```
f_ij = m_i^out * m_j^in * Q(d_ij)
```

- `f_ij`: observed flow from node *i* to node *j*
- `d_ij`: distance between node *i* and *j*
- `m_i^out`, `m_j^in`: latent node-specific properties (analogous to "mass")
- `Q(d)`: deterrence function, which decreases with distance

The goal is to **recover `m_i^out`, `m_j^in`, and `Q(d)`** from the flow and distance matrices.

---

## 🔧 Features

- Self-consistent iterative estimation of mass and deterrence
- Flexible binning of distance values into `Q` intervals
- Supports arbitrary OD matrices with asymmetric flows
- Designed for integration with international trade or spatial network data

---

## 🧾 Input Format

The package expects the following data structures in Python:

### `od_data`: Origin-Destination Flow Dictionary
```python
{
    "USA": {"CHN": 100, "DEU": 70},
    "CHN": {"USA": 50, "JPN": 30},
    ...
}
```

### `dist_data`: Distance Dictionary
```python
{
    "USA": {"CHN": 8000, "DEU": 7000},
    "CHN": {"USA": 8000, "JPN": 1500},
    ...
}
```

Each key is a node, with values indicating pairwise distances. This can represent geographic distance, cost, time, etc.

---

## 🚀 Usage

```python
from scgravity import filter_data, create_q_bin, calculate_mass

# Step 1: Clean flow matrix to only include valid distances
od_data_clean = filter_data(od_data, dist_data)

# Step 2: Bin the distance data into Q(d) intervals
q_bin = create_q_bin(od_data_clean, dist_data, each_num=500)

# Step 3: Infer m_in, m_out, Q(d)
m_in, m_out, Q_hist, Q_std = calculate_mass(od_data_clean, q_bin)
```

- `m_in`, `m_out`: dictionaries mapping node names to inferred mass values
- `Q_hist`: list of Q values per distance bin
- `Q_std`: standard deviation of Q values per bin

---

## 📈 Plotting Q(d): The Deterrence Function

You can visualize the learned `Q(d)` function (distance deterrence effect) as:

```python
import matplotlib.pyplot as plt

bin_mid = q_bin["bin_mid"]  # midpoints of each distance bin

plt.figure(figsize=(7,4))
plt.plot(bin_mid, Q_hist, marker='o')
plt.xlabel("Distance (d)")
plt.ylabel("Q(d)")
plt.title("Estimated Deterrence Function Q(d)")
plt.grid(True)
plt.tight_layout()
plt.show()
```

This gives you a graph of how the probability or strength of flow decreases with distance, as inferred from your data.

---

## 📂 Output Example

```python
print(m_out["USA"])     # e.g. 1.25
print(Q_hist[3])        # deterrence value for bin 3
```

You can use the inferred masses and Q function to reconstruct or simulate flows:
```python
f_est_ij = m_out["USA"] * m_in["CHN"] * Q_hist[q_bin["call_dic"]["USA"]["CHN"]]
```

---

## 📄 License

This project is licensed under the MIT License.
