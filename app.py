# app_unit_circle_clickable.py
import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Unit Circle Interaktif", layout="centered")

st.title("🧭 Unit Circle Interaktif")
st.write("""
Klik titik pada *Unit Circle* atau gunakan slider di bawah untuk memilih sudut tertentu.
Aplikasi ini menampilkan *kuadran, sudut relasi terhadap sumbu-x, serta nilai sin, cos, dan tan*.
""")

# --- Fungsi bantu ---
def get_quadrant(angle):
    if 0 < angle < 90:
        return "Kuadran I"
    elif 90 < angle < 180:
        return "Kuadran II"
    elif 180 < angle < 270:
        return "Kuadran III"
    elif 270 < angle < 360:
        return "Kuadran IV"
    elif angle in [0, 90, 180, 270, 360]:
        return "Berada di sumbu"
    else:
        return "-"

def reference_angle(angle):
    angle_mod = angle % 360
    if angle_mod <= 90:
        return angle_mod
    elif angle_mod <= 180:
        return 180 - angle_mod
    elif angle_mod <= 270:
        return angle_mod - 180
    else:
        return 360 - angle_mod

# --- Titik sudut utama ---
angles_deg = list(range(0, 360, 30))
angles_rad = [np.deg2rad(a) for a in angles_deg]
points_x = [np.cos(a) for a in angles_rad]
points_y = [np.sin(a) for a in angles_rad]

# --- Buat plot Unit Circle ---
theta = np.linspace(0, 2*np.pi, 360)
circle_x = np.cos(theta)
circle_y = np.sin(theta)

fig = go.Figure()

# Tambahkan warna kuadran
fig.add_shape(type="rect", x0=0, y0=0, x1=1.2, y1=1.2, fillcolor="rgba(0,255,0,0.1)", line_width=0)
fig.add_shape(type="rect", x0=-1.2, y0=0, x1=0, y1=1.2, fillcolor="rgba(0,0,255,0.1)", line_width=0)
fig.add_shape(type="rect", x0=-1.2, y0=-1.2, x1=0, y1=0, fillcolor="rgba(255,0,0,0.1)", line_width=0)
fig.add_shape(type="rect", x0=0, y0=-1.2, x1=1.2, y1=0, fillcolor="rgba(255,255,0,0.1)", line_width=0)

# Lingkaran utama
fig.add_trace(go.Scatter(x=circle_x, y=circle_y, mode="lines", line=dict(color="black"), showlegend=False))

# Titik-titik sudut utama (klikable)
fig.add_trace(go.Scatter(
    x=points_x,
    y=points_y,
    mode="markers+text",
    text=[f"{a}°" for a in angles_deg],
    textposition="top center",
    marker=dict(size=10, color="black"),
    hovertemplate="Sudut: %{text}<extra></extra>",
    name="Sudut",
))

# Sumbu X dan Y
fig.add_shape(type="line", x0=-1.2, x1=1.2, y0=0, y1=0, line=dict(color="gray", width=1))
fig.add_shape(type="line", x0=0, x1=0, y0=-1.2, y1=1.2, line=dict(color="gray", width=1))

fig.update_layout(
    width=600, height=600,
    margin=dict(l=20, r=20, t=20, b=20),
    xaxis=dict(range=[-1.3, 1.3], visible=False),
    yaxis=dict(range=[-1.3, 1.3], visible=False),
    clickmode='event+select',
    showlegend=False
)

# --- Ambil sudut yang dipilih (dari klik atau slider) ---
selected_angle_deg = angle_deg_from_click = None

# --- Tangkap klik pengguna ---
click_data = st.plotly_chart(fig, use_container_width=True, on_select="rerun", key="unit_circle")

# --- Slider fallback ---
slider_angle_deg = st.slider("Atau pilih sudut dengan slider:", 0, 360, 30, step=1)

# --- Tentukan sudut yang akan digunakan ---
if click_data and click_data["selection"]["points"]:
    point_idx = click_data["selection"]["points"][0]["point_index"]
    angle_deg_from_click = angles_deg[point_idx]
    angle_deg = angle_deg_from_click
else:
    angle_deg = slider_angle_deg

# --- Tambahkan visualisasi garis trigonometri ke grafik ---
angle_rad_selected = np.deg2rad(angle_deg)
x_point = np.cos(angle_rad_selected)
y_point = np.sin(angle_rad_selected)
tan_val_selected = np.tan(angle_rad_selected)

# Batasi panjang tangen agar visualisasi tetap baik
tan_display_limit = 1.5
if abs(tan_val_selected) > tan_display_limit:
    tan_val_display = np.sign(tan_val_selected) * tan_display_limit
else:
    tan_val_display = tan_val_selected

# Garis Radius (Terminal)
fig.add_trace(go.Scatter(x=[0, x_point], y=[0, y_point], mode="lines", line=dict(color="black", width=2), name="Radius"))
# Garis Sinus (merah)
fig.add_trace(go.Scatter(x=[x_point, x_point], y=[0, y_point], mode="lines", line=dict(color="red", width=3, dash='dash'), name="Sin"))
# Garis Cosinus (biru)
fig.add_trace(go.Scatter(x=[0, x_point], y=[0, 0], mode="lines", line=dict(color="blue", width=3, dash='dash'), name="Cos"))
# Garis Tangen (hijau) - hanya jika cos != 0
if abs(x_point) > 1e-9:
    fig.add_trace(go.Scatter(x=[1, 1], y=[0, tan_val_display], mode="lines", line=dict(color="green", width=3, dash='dash'), name="Tan"))
    # Garis bantu untuk tangen
    fig.add_trace(go.Scatter(x=[0, 1.2 if x_point > 0 else -1.2], y=[0, (1.2 if x_point > 0 else -1.2) * tan_val_selected], mode="lines", line=dict(color="gray", width=1, dash='dot')))

# Tampilkan kembali grafik yang sudah diperbarui
st.plotly_chart(fig, use_container_width=True, key="unit_circle_updated")

# --- Jika ada klik dari grafik ---
if click_data and click_data["selection"]["points"]:
    point_idx = click_data["selection"]["points"][0]["point_index"]
    angle_deg = angles_deg[point_idx]

# --- Hitung nilai trigonometri ---
angle_rad = np.deg2rad(angle_deg)
quadrant = get_quadrant(angle_deg % 360)
ref_angle = reference_angle(angle_deg)
sin_val = np.sin(angle_rad)
cos_val = np.cos(angle_rad)
tan_val = np.tan(angle_rad) if cos_val != 0 else "Tidak terdefinisi"

# --- Info Sudut ---
st.subheader("📘 Informasi Sudut")
st.write(f"*Sudut yang dipilih:* {angle_deg}°")
st.write(f"*Kuadran:* {quadrant}")
st.write(f"*Sudut relasi terhadap sumbu x:* {ref_angle}°")
st.write(f"*sin(θ) =* {sin_val:.3f}")
st.write(f"*cos(θ) =* {cos_val:.3f}")
st.write(f"*tan(θ) =* {tan_val if isinstance(tan_val, str) else f'{tan_val:.3f}'}")

st.markdown("---")
st.caption("Dikembangkan untuk membantu siswa memahami konsep sudut dan relasinya pada Unit Circle 🌐")