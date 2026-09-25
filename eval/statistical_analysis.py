"""
eval/statistical_analysis.py
------------------------------
Script Analisis Statistik Berpasangan & Audit Latency untuk Skripsi:
1. Uji Statistik Berpasangan: Wilcoxon Signed-Rank Test (RAG vs OKF paired latency).
2. Rank-Biserial Correlation (Effect Size r).
3. Statistik Deskriptif Lengkap: Median, Interquartile Range (IQR), Mean, StdDev.
4. Analisis Outlier (Tukey's Fences Q3 + 1.5*IQR dan Threshold > 100s).
5. Breakdown Latensi per 5 Kategori Kueri.
6. Analisis Token Count Balancing (Mean Prompt Tokens RAG vs OKF).
"""

import sys
import json
import numpy as np
from scipy import stats
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = Path(__file__).resolve().parent
PROFILE_RAG_FILE = BASE_DIR / "profile_rag.json"
PROFILE_OKF_FILE = BASE_DIR / "profile_okf.json"
DATASET_FILE     = BASE_DIR / "test_dataset_extended_N40.json"
OUTPUT_STATS_FILE= BASE_DIR / "statistical_results.json"


def compute_rank_biserial_effect_size(rag_lat, okf_lat):
    """
    Hitung Rank-Biserial Correlation (r) untuk Wilcoxon Signed-Rank Test.
    Formula: r = 1 - (4 * W) / (N * (N + 1))  [jika W = min(R+, R-)]
    Atau r = (R+ - R-) / (R+ + R-)
    """
    diffs = rag_lat - okf_lat
    non_zero = diffs[diffs != 0]
    if len(non_zero) == 0:
        return 0.0
    
    ranks = stats.rankdata(np.abs(non_zero))
    pos_ranks = np.sum(ranks[non_zero > 0])
    neg_ranks = np.sum(ranks[non_zero < 0])
    total_ranks = pos_ranks + neg_ranks
    
    if total_ranks == 0:
        return 0.0
    return float((pos_ranks - neg_ranks) / total_ranks)


def analyze_performance():
    print("=" * 80)
    print("  ANALISIS STATISTIK BERPASANGAN (PAIRED WILCOXON) & EFFECT SIZE (r)")
    print("=" * 80 + "\n")

    if not PROFILE_RAG_FILE.exists() or not PROFILE_OKF_FILE.exists():
        print("ERROR: File profile_rag.json atau profile_okf.json belum ditemukan.")
        return

    rag_data = json.loads(PROFILE_RAG_FILE.read_text(encoding="utf-8"))
    okf_data = json.loads(PROFILE_OKF_FILE.read_text(encoding="utf-8"))
    accuracy_data = json.loads(DATASET_FILE.read_text(encoding="utf-8"))

    rag_latencies = np.array(rag_data.get("latency_samples", []))
    okf_latencies = np.array(okf_data.get("latency_samples", []))
    rag_tokens    = rag_data.get("prompt_tokens_samples", [])
    okf_tokens    = okf_data.get("prompt_tokens_samples", [])
    queries       = accuracy_data.get("queries", [])[:len(rag_latencies)]

    min_len = min(len(rag_latencies), len(okf_latencies))
    rag_lat = rag_latencies[:min_len]
    okf_lat = okf_latencies[:min_len]

    # 1. Wilcoxon Signed-Rank Test & Rank-Biserial Effect Size
    res_wilcoxon = stats.wilcoxon(rag_lat, okf_lat)
    p_value = float(res_wilcoxon.pvalue)
    stat_w = float(res_wilcoxon.statistic)
    r_effect_size = compute_rank_biserial_effect_size(rag_lat, okf_lat)

    # 2. Descriptive Stats & Tukey's Fences Outlier Audit
    rag_q75, rag_q25 = np.percentile(rag_lat, [75, 25])
    rag_iqr = rag_q75 - rag_q25
    rag_upper_fence = rag_q75 + 1.5 * rag_iqr
    rag_outliers = rag_lat[rag_lat > rag_upper_fence]

    okf_q75, okf_q25 = np.percentile(okf_lat, [75, 25])
    okf_iqr = okf_q75 - okf_q25
    okf_upper_fence = okf_q75 + 1.5 * okf_iqr
    okf_outliers = okf_lat[okf_lat > okf_upper_fence]

    rag_clean = rag_lat[rag_lat <= rag_upper_fence]
    okf_clean = okf_lat[okf_lat <= okf_upper_fence]

    rag_med = float(np.median(rag_lat))
    okf_med = float(np.median(okf_lat))

    print("📊 STATISTIK DESKRIPTIF AKURAT (MEDIAN & IQR):")
    print(f"  • SYSTEM RAG -> Median: {rag_med:.2f}s | IQR: {rag_iqr:.2f}s | Mean: {np.mean(rag_lat):.2f}s (Clean: {np.mean(rag_clean):.2f}s)")
    print(f"  • SYSTEM OKF -> Median: {okf_med:.2f}s | IQR: {okf_iqr:.2f}s | Mean: {np.mean(okf_lat):.2f}s (Clean: {np.mean(okf_clean):.2f}s)")
    print(f"  • Outlier Tukey (Q3 + 1.5*IQR): RAG {len(rag_outliers)} sampel, OKF {len(okf_outliers)} sampel")

    print(f"\n🧪 WILCOXON SIGNED-RANK TEST (PAIRED DESIGN):")
    print(f"  • Statistic W : {stat_w}")
    print(f"  • p-value     : {p_value:.6f}")
    print(f"  • Effect Size r (Rank-Biserial): {r_effect_size:+.4f}")
    if p_value < 0.05:
        print("  • Kesimpulan  : 🟢 Perbedaan latensi RAG vs OKF BERMAKNA SECARA STATISTIK (p < 0.05)")
    else:
        print("  • Kesimpulan  : 🟡 Perbedaan latensi TIDAK SIGNIFIKAN SECARA STATISTIK (p >= 0.05)")

    # 3. Token Balancing Audit
    avg_rag_tok = sum(rag_tokens) / len(rag_tokens) if rag_tokens else 0
    avg_okf_tok = sum(okf_tokens) / len(okf_tokens) if okf_tokens else 0
    diff_pct = abs(avg_rag_tok - avg_okf_tok) / max(avg_rag_tok, avg_okf_tok) * 100 if max(avg_rag_tok, avg_okf_tok) > 0 else 0
    
    print(f"\n📐 AUDIT TOKEN-COUNT BALANCING:")
    print(f"  • Mean RAG Prompt Tokens : {avg_rag_tok:.1f} tokens")
    print(f"  • Mean OKF Prompt Tokens : {avg_okf_tok:.1f} tokens")
    print(f"  • Perbedaan Selisih Token: {diff_pct:.1f}%")

    # 4. Category Breakdown
    cat_latencies = {}
    for idx, q in enumerate(queries):
        cat = q.get("category", "unknown")
        if cat not in cat_latencies:
            cat_latencies[cat] = {"rag": [], "okf": []}
        cat_latencies[cat]["rag"].append(float(rag_lat[idx]))
        cat_latencies[cat]["okf"].append(float(okf_lat[idx]))

    cat_breakdown_summary = {}
    print("\n📂 BREAKDOWN LATENSI PER-KATEGORI KUERI:")
    print(f"  {'Kategori Kueri':<25} | {'RAG Median':<12} | {'OKF Median':<12} | {'Selisih (OKF vs RAG)':<20}")
    print("-" * 75)
    for cat, val in cat_latencies.items():
        r_m = float(np.median(val["rag"])) if val["rag"] else 0.0
        o_m = float(np.median(val["okf"])) if val["okf"] else 0.0
        diff = o_m - r_m
        cat_breakdown_summary[cat] = {
            "rag_median_sec": round(r_m, 2),
            "okf_median_sec": round(o_m, 2),
            "diff_sec": round(diff, 2)
        }
        print(f"  {cat:<25} | {r_m:<12.2f}s | {o_m:<12.2f}s | {diff:+.2f}s")

    # Output payload
    summary_payload = {
        "wilcoxon_w": stat_w,
        "p_value": p_value,
        "statistically_significant": p_value < 0.05,
        "rank_biserial_r": round(r_effect_size, 4),
        "rag": {
            "median_sec": round(rag_med, 2),
            "iqr_sec": round(rag_iqr, 2),
            "mean_sec": round(float(np.mean(rag_lat)), 2),
            "std_sec": round(float(np.std(rag_lat)), 2),
            "mean_clean_sec": round(float(np.mean(rag_clean)), 2),
            "outliers_count": len(rag_outliers),
            "mean_prompt_tokens": round(avg_rag_tok, 1)
        },
        "okf": {
            "median_sec": round(okf_med, 2),
            "iqr_sec": round(okf_iqr, 2),
            "mean_sec": round(float(np.mean(okf_lat)), 2),
            "std_sec": round(float(np.std(okf_lat)), 2),
            "mean_clean_sec": round(float(np.mean(okf_clean)), 2),
            "outliers_count": len(okf_outliers),
            "mean_prompt_tokens": round(avg_okf_tok, 1)
        },
        "token_difference_pct": round(diff_pct, 2),
        "category_breakdown": cat_breakdown_summary
    }

    OUTPUT_STATS_FILE.write_text(json.dumps(summary_payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n✅ Results saved to {OUTPUT_STATS_FILE.resolve()}")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    analyze_performance()
