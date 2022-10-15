import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

sns.set_theme()
sns.set_style("whitegrid", {'grid.linestyle': '--', "xtick.major.size": 8, "ytick.major.size": 8})


plt.rc('font', size=12)  # controls default text sizes
plt.rc('axes', titlesize=15)  # fontsize of the axes title
plt.rc('figure', titlesize=15)  # fontsize of the figure title

metric_map = {"mse": "Mean Square Error (MSE)", "k_mse": "Top-k MSE (k=50)"}

def plot_comparison_vary_k(metric="mse"):
    df = pd.read_csv("experiments/new_1_exp3_varyK_metrics_k2-256_m32.csv")
    x = np.array([2, 4, 8, 16, 32, 64, 128, 256])
    fig = plt.figure(figsize=(6,5))

    colors = ["darkcyan", "c", "peru", "saddlebrown"]
    markers = ["o", "s", "x", "v", "d", "o", ">", ".", "."]

    ax = fig.add_subplot(111)
    ax.spines['bottom'].set_color("black")
    ax.spines['top'].set_color("black")
    ax.spines['left'].set_color("black")
    ax.spines['right'].set_color("black")

    for i, freq_oracle in enumerate(df["freq_oracle"].unique()):
        filtered_df = df[df["freq_oracle"] == freq_oracle]
        means = filtered_df.groupby("info", sort=False).mean()[metric]
        ax.plot(x.astype("str"), means, marker=markers[i], color=colors[i], mfc="white", ms=10, linewidth=2.5, label=freq_oracle)

    ax.set_yscale('log')
    ax.tick_params(axis='both', which='major', labelsize=16)
    ax.set_xlabel("Number of Hash Functions ($r$)", fontsize=18)
    ax.set_ylabel("Log(MSE)", fontsize=18)

    plt.legend(frameon=False)
    plt.tight_layout()
    plt.grid(visible=False)
    plt.show()
    # plt.savefig('experiments/figs/new_1_exp3_varyK_metrics_k2-256_m32.eps', format='eps')

def plot_comparison_vary_m(metric="mse"):
    df = pd.read_csv("experiments/new_1_exp2_varyM_metrics_k4_m4-1024.csv")

    x = np.array([4, 8, 16, 32, 64, 128, 256, 512, 1024])
    fig = plt.figure(figsize=(6,5))
    markers = ["o", "s", "x", "v", "d", "o", ">", ".", "."]
    colors = ["darkcyan", "c", "peru", "saddlebrown"]

    ax = fig.add_subplot(111)
    ax.spines['bottom'].set_color("black")
    ax.spines['top'].set_color("black")
    ax.spines['left'].set_color("black")
    ax.spines['right'].set_color("black")

    for i, freq_oracle in enumerate(df["freq_oracle"].unique()):
        filtered_df = df[df["freq_oracle"] == freq_oracle]
        means = filtered_df.groupby("info", sort=False).mean()[metric]
        ax.plot(x.astype("str"), means, marker=markers[i], color=colors[i], mfc="white", ms=10, linewidth=2.5,
                label=freq_oracle)

    ax.set_yscale('log')
    ax.set_xlabel("Size of Sketch Vector ($c$)", fontsize=18)
    ax.set_ylabel("Log(MSE)", fontsize=18)
    ax.tick_params(axis='both', which='major', labelsize=16)
    plt.legend(frameon=False)
    plt.tight_layout()
    plt.grid(visible=False)
    plt.show()
    # plt.savefig('experiments/figs/new_1_exp2_varyM_metrics_k4_m4-1024.eps', format='eps')

def plot_comparison_vary_d(metric="mse", same_plot=True):
    df = pd.read_csv("./experiments/new_5_exp4_varyD_all_k4_m128.csv")
    x = np.array([20000, 40000, 60000, 80000, 100000])
    fig = plt.figure(figsize=(6,5))
    colors = ["darkcyan", "c", "peru", "saddlebrown"]
    markers = ["o", "s", "x", "v", "d", "o", ">", ".", "."]

    ax = fig.add_subplot(111)
    ax.spines['bottom'].set_color("black")
    ax.spines['top'].set_color("black")
    ax.spines['left'].set_color("black")
    ax.spines['right'].set_color("black")
    metrics = ["mse"]

    for j,metric in enumerate(metrics):
        for i, freq_oracle in enumerate(df["freq_oracle"].unique()):
            filtered_df = df[df["freq_oracle"] == freq_oracle]
            means = filtered_df.groupby("info", sort=False).mean()[metric]
            ax.plot(x, means, marker=markers[i], color=colors[i], mfc="white", ms=10, linewidth=2.5, label=freq_oracle)

        ax.set_xlabel("Domain Size ($d$)", fontsize=18)
        ax.set_ylabel("Log(MSE)", fontsize=18)
        ax.set_yscale('log')
        ax.tick_params(axis="x", labelsize=16)
        ax.tick_params(axis="y", labelsize=16)

    plt.ylim(pow(10,-3),pow(10,0))
    plt.grid(visible=False)
    plt.legend(frameon=False)
    plt.tight_layout()
    plt.plot()
    plt.show()
    # plt.savefig('experiments/figs/new_5_exp4_varyD_all_k4_m128.eps', format='eps', bbox_inches="tight")

def plot_comparison_vary_eps():
    df = pd.read_csv("experiments/new_3_all_k4_m128.csv")
    x = [2, 4, 8, 16, 32, 64, 128]
    fig = plt.figure(figsize=(6, 5))
    ax = fig.add_subplot(111)
    ax.spines['bottom'].set_color("black")
    ax.spines['top'].set_color("black")
    ax.spines['left'].set_color("black")
    ax.spines['right'].set_color("black")

    colors = ["darkcyan", "c", "peru", "saddlebrown"]

    markers = ["o", "s", "x", "v", "d", "o", ">", ".", "."]
    for i, freq_oracle in enumerate(df["freq_oracle"].unique()):
        filtered_df = df[df["freq_oracle"] == freq_oracle]
        means = filtered_df.groupby("info", sort=False).mean()["mse"]
        ax.plot(np.arange(len(x)), means, marker=markers[i], color=colors[i], mfc="white", ms=10, linewidth=2.5, label=freq_oracle)

    plt.xlim(1,len(x)-1)
    plt.ylim(pow(10,-5),pow(10,1))
    plt.xticks(np.arange(len(x)), x)
    plt.xlabel("Privacy Budget ($\epsilon$)", fontsize=18)
    plt.ylabel("Mean Squared Error (MSE)")
    ax.set_yscale('log')
    ax.tick_params(axis='both', which='major', labelsize=16)
    plt.tight_layout()
    plt.grid(visible=False)
    plt.legend(fontsize=18, frameon=False)
    plt.show()
    # plt.savefig('experiments/figs/new_3_all_k4_m128.eps', format='eps')

def plot_comparison_vary_items(n, dataLen, time_metric):
    df = pd.read_csv("experiments/new_time_repeat10_item1-10000.csv")
    x = [1, 10, 100, 1000, 10000]
    fig = plt.figure(figsize=(6, 5))
    ax = fig.add_subplot(111)
    ax.spines['bottom'].set_color("black")
    ax.spines['top'].set_color("black")
    ax.spines['left'].set_color("black")
    ax.spines['right'].set_color("black")

    colors = ["olive","darkcyan", "c", "peru", "saddlebrown"]
    markers = ["d", "o", "s", "x", "v",  "o", ">", ".", "."]
    for i, freq_oracle in enumerate(df["freq_oracle"].unique()):
        filtered_df = df[df["freq_oracle"] == freq_oracle]
        if time_metric == "total_time":
            server_means = filtered_df.groupby("info", sort=False).mean()["server_time"]
            client_means = filtered_df.groupby("info", sort=False).mean()["client_time"]/n
            means = server_means + client_means
        else:
            means = filtered_df.groupby("info", sort=False).mean()[time_metric]
        ax.plot(np.arange(len(x)), means, marker=markers[i], color=colors[i], mfc="white", ms=10, linewidth=2.5, label=freq_oracle)

    plt.xlim(1,len(x)-1)
    plt.xticks(np.arange(len(x)), x)
    plt.xlabel("Estimation Number", fontsize=18)
    plt.ylabel("Time",fontsize=18)
    ax.tick_params(axis='both', which='major', labelsize=16)
    plt.tight_layout()
    plt.grid(visible=False)
    plt.legend(fontsize=18, frameon=False)
    plt.show()
    # plt.savefig('experiments/figs/new_time_repeat10_item1-1000.eps', format='eps')

def compare_mse():
    df = pd.read_csv("experiments/new_3_all_k4_m128.csv")

    mse = {}
    for i, freq_oracle in enumerate(df["freq_oracle"].unique()):
        filtered_df = df[df["freq_oracle"] == freq_oracle]
        means = filtered_df.groupby("info", sort=False).mean()["mse"]
        mse[freq_oracle]=np.array(means)

    result1 = mse["PrivSketch"]/mse["Multi-PCMS-Mean"]
    result2 = mse["PrivSketch"]/mse["Multi-PCMS-Min"]
    print(result1)
    print(result2)

# ----------------------------------------------------
plot_comparison_vary_eps()
plot_comparison_vary_m("mse")
plot_comparison_vary_k("mse")
plot_comparison_vary_d("mse")
plot_comparison_vary_items("server_time")
# compare_mse()