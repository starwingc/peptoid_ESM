"""Canonical method names and colors for all cross-method comparison plots
in this Analysis/ folder.

See PLOTTING_STYLE.md in this same folder for the full style guide and the
rationale behind the naming/color choices. Import from here instead of
re-declaring a local ``method_colors`` dict so that every figure in the
paper uses the same name and the same color for the same method.

Usage:
    from plotting_style import METHOD_COLORS, METHOD_ORDER

    method_colors = {k: METHOD_COLORS[k] for k in ["Plain MD", "EE", "HREX", "REDS"]}
"""

# Canonical display order (also the legend order convention: enhanced-sampling
# methods first in the order they were introduced, metadynamics last).
METHOD_ORDER = [
    "Plain MD",
    "EE",
    "HREX",
    "REDS",
    "META-OMG",
    "META-OMG8REP",
    "META-OPH",
    "META-OPP",
    "META-OPPC",
    "META-OPPC8REP",
]

# tab10 base colors for the four core methods, plus tab10 purple/brown for the
# 8-replica metadynamics runs. META-OMG (single-replica) uses the tab20 "light"
# pairing of the META-OMG8REP purple (#9467bd -> #c5b0d5) so that the
# single-replica and 8-replica variants of the same collective variable read as
# the same color family at a glance. META-OPPC (single replica) uses the
# tab20 light-brown pairing of META-OPPC8REP (#8c564b -> #c49c94), per the
# convention documented above and in PLOTTING_STYLE.md.
#
# META-OPH (omega+phi) and META-OPP (omega+phi+psi) are single-replica PBMetaD
# CV combinations that only ever appear in the SI (never compared against an
# 8-replica counterpart of the same CV set), so they follow the "Adding a new
# method later" rule in PLOTTING_STYLE.md as new base methods: the next two
# unused tab10 colors, in tab10's canonical order right after the brown
# (META-OPPC8REP) slot already claimed by this project -- tab10 pink and
# tab10 gray. Flagged here since these two colors are a first-time addition
# with no prior precedent in this project; revisit if the manuscript authors
# want a different pairing.
METHOD_COLORS = {
    "Plain MD":      "#1f77b4",  # tab10 blue
    "EE":            "#2ca02c",  # tab10 green
    "HREX":          "#ff7f0e",  # tab10 orange
    "REDS":          "#d62728",  # tab10 red
    "META-OMG":      "#c5b0d5",  # tab20 light purple (single replica)
    "META-OMG8REP":  "#9467bd",  # tab10 purple (8 replicas)
    "META-OPH":      "#e377c2",  # tab10 pink (single replica, SI-only)
    "META-OPP":      "#7f7f7f",  # tab10 gray (single replica, SI-only)
    "META-OPPC":     "#c49c94",  # tab20 light brown (single replica)
    "META-OPPC8REP": "#8c564b",  # tab10 brown (8 replicas)
}

# ---------------------------------------------------------------------------
# Figure style shared by every "grid of panels" comparison figure (error vs.
# tau, population vs. tau, stationary population vs. lagtime, implied
# timescale, autocorrelation, ...). Modeled on plot_error_grid() in
# error_over_time_8_conform.ipynb, the reference figure this style matches.
# ---------------------------------------------------------------------------
# Canonical colors for the eight backbone cis/trans conformer states, used by
# any per-METHOD panel grid that overlays all 8 states as separate curves
# within one panel (e.g. stationary_population_8_conform.ipynb's
# plot_method_grid). This is a distinct color dimension from METHOD_COLORS
# above -- the two are never both needed as a legend in the same figure,
# since a per-method-panel figure labels each panel by method name (title)
# and colors its 8 curves by state, while a per-state-panel figure (e.g.
# plot_state_grid) does the opposite. Matches the matplotlib tab10 cycle
# (the previously-implicit default), now pinned down explicitly by state
# label so every panel of every such figure colors "ttt" (etc.) identically.
STATE_ORDER = ["ccc", "cct", "ctc", "ctt", "tcc", "tct", "ttc", "ttt"]
STATE_COLORS = {
    "ccc": "#1f77b4",
    "cct": "#ff7f0e",
    "ctc": "#2ca02c",
    "ctt": "#d62728",
    "tcc": "#9467bd",
    "tct": "#8c564b",
    "ttc": "#e377c2",
    "ttt": "#7f7f7f",
}

# Canonical colors for the three per-residue (omega-angle) cis/trans series,
# used by any per-METHOD panel grid that overlays all 3 residues as separate
# curves within one panel (e.g. error_over_time_res_all.ipynb's
# plot_method_grid_error_res, population_over_time_res_all.ipynb's
# plot_method_grid_population_res). Residue-wise counterpart of STATE_COLORS
# above -- every such panel, in every such figure, colors "Residue 0"
# identically. Several existing notebooks already re-declare this same dict
# literally as a local `RES_COLORS`; this is the shared source of truth new
# code should import instead of re-declaring.
RES_ORDER = [0, 1, 2]
RES_COLORS = {
    0: "#1f77b4",
    1: "#ff7f0e",
    2: "#2ca02c",
}

TITLE_FONTSIZE = 14        # per-panel title (italic)
TICK_FONTSIZE = 16         # per-panel tick labels
AXIS_LABEL_FONTSIZE = 20   # figure-level shared x/y label (fig.supxlabel/supylabel)
LEGEND_FONTSIZE = 16       # the one shared top legend
LINEWIDTH = 1.5            # data lines
LEGEND_LINEWIDTH = 3.0     # legend line swatches (thicker than the data lines so they read at a glance)


def style_panel(ax, title, tick_fontsize=TICK_FONTSIZE, title_fontsize=TITLE_FONTSIZE):
    """Apply the shared per-panel look: italic title, large tick labels.

    `title` may contain a literal ``\\n`` to wrap onto a second line when the
    panel title is a method name rather than a short conformation label
    (e.g. ``"META-OMG8REP\\nPopulation"``) -- keep the same fontsize rather
    than shrinking it to fit on one line.
    """
    ax.set_title(title, fontstyle='italic', fontsize=title_fontsize)
    ax.tick_params(axis='both', which='major', labelsize=tick_fontsize)


def add_grid_legend(fig, ax_for_handles, ncol=None, fontsize=LEGEND_FONTSIZE):
    """Draw the one shared horizontal legend above a grid figure, reading
    its handles/labels off one already-plotted panel (usually axes[0])."""
    handles, labels = ax_for_handles.get_legend_handles_labels()
    leg = fig.legend(
        handles, labels,
        loc='upper center', bbox_to_anchor=(0.5, 1.0), ncol=ncol or len(labels),
        frameon=False, handlelength=1.5, handletextpad=0.5, columnspacing=1.0,
        fontsize=fontsize,
    )
    for line in leg.get_lines():
        line.set_linewidth(LEGEND_LINEWIDTH)
    return leg
