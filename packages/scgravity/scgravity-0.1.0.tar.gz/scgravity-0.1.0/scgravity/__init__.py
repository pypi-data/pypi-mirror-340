import numpy as np
import bisect
from typing import Dict, Tuple, List

def get_keys_with_second_key(od_data: Dict[str, Dict[str, float]], target_key: str) -> List[str]:
    """
    Returns all first keys in od_data that have target_key as their second key.
    """
    return [i for i in od_data if target_key in od_data.get(i, {})]

def filter_data(od_data: Dict[str, Dict[str, float]], dist_data: Dict[str, Dict[str, float]]) -> Dict[str, Dict[str, float]]:
    """
    Cleans the od_data by removing all origins and destinations that do not exist in dist_data.
    """
    common_nodes = set(dist_data.keys())
    cleaned = {}
    for i in od_data:
        if i in common_nodes:
            cleaned[i] = {j: od_data[i][j] for j in od_data[i] if j in common_nodes}
    return cleaned

def create_q_bin(od_data: Dict[str, Dict[str, float]], dist_data: Dict[str, Dict[str, float]], each_num: int = 500) -> Dict:
    """
    Sorts distance values and divides them into bins of specified size.
    """
    sts, eds, dis = [], [], []
    for i in od_data:
        for j in od_data[i]:
            if i in dist_data and j in dist_data[i]:
                sts.append(i)
                eds.append(j)
                dis.append(dist_data[i][j])

    if not dis:
        raise ValueError("No valid distances found between OD pairs.")

    arglist = np.argsort(dis)
    num_elements = len(arglist)
    binnum = max(1, num_elements // each_num)

    bin_mid, st_list, ed_list = [], [], []
    st_list = [sts[arg] for arg in arglist]
    ed_list = [eds[arg] for arg in arglist]
    st_ed = {i: {} for i in dist_data.keys()}
    left_list, right_list = [], []

    for i in range(binnum):
        mid_sum, mid_num = 0, 0
        start_idx = i * each_num
        end_idx = num_elements if i == binnum - 1 else (i + 1) * each_num

        for j in range(start_idx, end_idx):
            now_idx = j
            mid_sum += dis[arglist[now_idx]]
            mid_num += 1
            st_idx, ed_idx = st_list[now_idx], ed_list[now_idx]
            st_ed.setdefault(st_idx, {})[ed_idx] = i

        if mid_num:
            bin_mid.append(mid_sum / mid_num)
            left_list.append(dis[arglist[start_idx]])
            right_list.append(dis[arglist[end_idx - 1]])

    return {"bin_mid": bin_mid, "call_dic": st_ed, "bin_left": left_list, "bin_right": right_list}

def cal_bindex(now_dist: float, q_bin: Dict) -> int:
    """
    Calculates the bin index for a given distance using binary search.
    """
    left_list = q_bin['bin_left']
    index = bisect.bisect_left(left_list, now_dist)
    return max(0, index - 1)

def cal_real_infer_sum(od_data: Dict[str, Dict[str, float]], m_in, m_out, Q_hist, Q_call) -> Tuple[float, float]:
    """
    Calculates the real and inferred totals based on the given data and parameters.
    """
    real_tot = 0
    infer_tot = 0
    for i in od_data:
        for j in od_data[i]:
            if i in m_out and j in m_in and i in Q_call and j in Q_call[i]:
                real_tot += od_data[i][j]
                infer_tot += m_out[i] * m_in[j] * Q_hist[Q_call[i][j]]
    return real_tot, infer_tot

def calculate_mass(od_data: Dict[str, Dict[str, float]], q_bin: Dict, iter_step: int = 10) -> Tuple[Dict, Dict, List, List]:
    """
    Calculates node masses and deterrence function Q from OD and distance data.
    """
    Q_call = q_bin["call_dic"]
    bin_mid = q_bin["bin_mid"]
    binnum = len(bin_mid)
    Q_hist = [1.0] * binnum

    sum_out = {i: sum(od_data[i].values()) for i in od_data}
    second_keys = {j for i in od_data for j in od_data[i]}
    sum_in = {j: sum(od_data[i][j] for i in od_data if j in od_data[i]) for j in second_keys}

    M_out = {i: 1.0 for i in od_data}
    M_in = {j: 1.0 for j in second_keys}

    for _ in range(iter_step):
        tem_M_out = {
            i: sum_out[i] / sum(M_in[j] * Q_hist[Q_call[i][j]] for j in od_data[i] if j in M_in and j in Q_call[i] and i != j)
            if sum(M_in[j] * Q_hist[Q_call[i][j]] for j in od_data[i] if j in M_in and j in Q_call[i] and i != j) > 0 else 0
            for i in od_data
        }
        tem_M_in = {
            j: sum_in[j] / sum(M_out[i] * Q_hist[Q_call[i][j]] for i in get_keys_with_second_key(od_data, j) if i in M_out and j in Q_call[i] and i != j)
            if sum(M_out[i] * Q_hist[Q_call[i][j]] for i in get_keys_with_second_key(od_data, j) if i in M_out and j in Q_call[i] and i != j) > 0 else 0
            for j in second_keys
        }
        M_out, M_in = tem_M_out.copy(), tem_M_in.copy()

        new_Q, Q_num, new_Q_std = [0.0] * binnum, [0] * binnum, [0.0] * binnum
        for i in od_data:
            for j in od_data[i]:
                if i != j and i in M_out and j in M_in and i in Q_call and j in Q_call[i]:
                    b = Q_call[i][j]
                    val = od_data[i][j] / (M_out[i] * M_in[j])
                    new_Q[b] += val
                    new_Q_std[b] += val ** 2
                    Q_num[b] += 1

        Q_hist = [new_Q[i] / Q_num[i] if Q_num[i] else 0 for i in range(binnum)]
        Q_std = [((new_Q_std[i] / Q_num[i] - Q_hist[i] ** 2) / Q_num[i]) ** 0.5 if Q_num[i] else 0 for i in range(binnum)]

        real_tot, infer_tot = cal_real_infer_sum(od_data, M_in, M_out, Q_hist, Q_call)
        if infer_tot > 0:
            scale = real_tot / infer_tot
            Q_hist = [q * scale for q in Q_hist]
            Q_std = [q * scale for q in Q_std]

    Avg_Min = np.mean(list(M_in.values())) if M_in else 1
    Avg_Mout = np.mean(list(M_out.values())) if M_out else 1
    Max_Q = max(Q_hist) if Q_hist else 1

    Q_hist = [q / Max_Q for q in Q_hist]
    Q_std = [q / Max_Q for q in Q_std]

    norm = (Avg_Min * Avg_Mout * Max_Q * real_tot / infer_tot) ** 0.5 if infer_tot else 1
    M_in = {k: v * norm / Avg_Min for k, v in M_in.items()}
    M_out = {k: v * norm / Avg_Mout for k, v in M_out.items()}

    return M_in, M_out, Q_hist, Q_std

def calculate_sums(od_data: Dict[str, Dict[str, float]], q_bin: Dict) -> Tuple[Dict, Dict, List, List]:
    """
    Calculates flow-normalized Q from raw in/out sums.
    """
    Q_call = q_bin["call_dic"]
    bin_mid = q_bin["bin_mid"]
    binnum = len(bin_mid)

    sum_out = {i: sum(od_data[i].values()) for i in od_data}
    second_keys = {j for i in od_data for j in od_data[i]}
    sum_in = {j: sum(od_data[i][j] for i in od_data if j in od_data[i]) for j in second_keys}

    new_Q, Q_num, new_Q_std = [0.0] * binnum, [0] * binnum, [0.0] * binnum
    for i in od_data:
        for j in od_data[i]:
            if i != j and sum_out.get(i, 0) != 0 and sum_in.get(j, 0) != 0 and i in Q_call and j in Q_call[i]:
                b = Q_call[i][j]
                val = od_data[i][j] / (sum_out[i] * sum_in[j])
                new_Q[b] += val
                new_Q_std[b] += val ** 2
                Q_num[b] += 1

    Q_hist = [new_Q[i] / Q_num[i] if Q_num[i] > 0 else 0 for i in range(binnum)]
    Q_std = [((new_Q_std[i] / Q_num[i] - Q_hist[i] ** 2) / Q_num[i]) ** 0.5 if Q_num[i] > 0 else 0 for i in range(binnum)]

    real_tot, infer_tot = cal_real_infer_sum(od_data, sum_in, sum_out, Q_hist, Q_call)
    if infer_tot:
        Q_hist = [q * real_tot / infer_tot for q in Q_hist]
        Q_std = [q * real_tot / infer_tot for q in Q_std]

    return sum_in, sum_out, Q_hist, Q_std