import pickle

import cospar as cs
import scvelo as scv

from pyrovelocity.plot import denoised_umap


cs.logging.print_version()
cs.settings.verbosity = 2
cs.settings.data_path = "LARRY_data"  # A relative path to save data.
cs.settings.figure_path = "LARRY_figure"  # A relative path to save figures.
cs.settings.set_figure_params(
    format="png", figsize=[4, 3.5], dpi=75, fontsize=14, pointsize=2
)

adata_input = scv.read("larry_invitro_adata_with_scvelo_dynamicalvelocity.h5ad")
adata = scv.read("larry_invitro_adata_sub_raw.h5ad")
adata_cospar = scv.read(
    "LARRY_MultiTimeClone_Later_FullSpace0_t*2.0*4.0*6_adata_with_transition_map.h5ad"
)
adata_cytotrace = scv.read("larry_invitro_adata_sub_raw_withcytotrace.h5ad")

adata_uni_mono = scv.read("mono_unipotent_cells.h5ad")
adata_uni_mono = adata_uni_mono[adata_uni_mono.obs.state_info != "Centroid", :].copy()

adata_uni_neu = scv.read("neu_unipotent_cells.h5ad")
adata_uni_neu = adata_uni_neu[adata_uni_neu.obs.state_info != "Centroid", :].copy()

adata_uni_bifurcation = adata_uni_mono.concatenate(adata_uni_neu)

cs.pl.fate_potency(
    adata_cospar,
    used_Tmap="transition_map",
    map_backward=True,
    method="norm-sum",
    color_bar=True,
    fate_count=True,
)

with open("fig3_allcells_data_model2.pkl", "rb") as pk:
    result_dict = pickle.load(pk)
adata_model_pos_all = result_dict["adata_model_pos"]
v_map_all_all = result_dict["v_map_all"]
embeds_radian_all = result_dict["embeds_radian"]
fdri_all = result_dict["fdri"]
embed_mean_all = result_dict["embed_mean"]
# adata_input_all = scv.read("larry_allcells_top2000.h5ad")
adata_input_all = scv.read("fig3_larry_allcells_top2000_model2.h5ad")
adata_input_all.obs.cytotrace = adata_cytotrace.obs.cytotrace

with open("fig2_pancreas_data.pkl", "rb") as f:
    result_dict = pickle.load(f)
adata_model_pos = result_dict["adata_model_pos"]
v_map_all = result_dict["v_map_all"]
embeds_radian = result_dict["embeds_radian"]
fdri = result_dict["fdri"]
embed_mean = result_dict["embed_mean"]
adata = scv.read("fig2_pancreas_processed.h5ad")


fig = denoised_umap(
    adata_model_pos_all, adata_input_all, cell_state="state_info", n_jobs=30
)
fig.savefig(
    "larry_multifate_supp6.pdf",
    facecolor=fig.get_facecolor(),
    bbox_inches="tight",
    edgecolor="none",
    dpi=300,
)


fig2 = denoised_umap(adata_model_pos, adata, cell_state="clusters")
fig2.savefig(
    "pancreas_supp6.pdf",
    facecolor=fig2.get_facecolor(),
    bbox_inches="tight",
    edgecolor="none",
    dpi=300,
)