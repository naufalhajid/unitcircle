import streamlit as st
import numpy as np
import math
import plotly.graph_objects as go

st.set_page_config(page_title="Unit Circle Interaktif", layout="wide")

st.title("🧭 Unit Circle Interaktif")
st.write("""
Klik titik pada *Unit Circle* atau gunakan slider di bawah untuk memilih sudut tertentu.
Aplikasi ini menampilkan visualisasi geometris dan nilai dari keenam fungsi trigonometri.
""")

# --- Konstanta ---
TOLERANCE = 1e-9 # Toleransi untuk perbandingan floating point (menghindari pembagian dengan nol)

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

# --- Inisialisasi Session State --- 
if 'angle_deg' not in st.session_state:
    st.session_state.angle_deg = 30
if 'rad_mode' not in st.session_state:
    st.session_state.rad_mode = False

# --- Callback untuk sinkronisasi widget --- 
def update_angle():
    # Perbarui session state dengan nilai terbaru dari slider atau input angka
    st.session_state.angle_deg = st.session_state.get('angle_slider', st.session_state.angle_deg)
    st.session_state.angle_deg = st.session_state.get('angle_num_input', st.session_state.angle_deg)

# --- Titik sudut utama ---
angles_deg_30 = list(range(0, 360, 30))
angles_deg_45 = list(range(0, 360, 45))
angles_deg = sorted(list(set(angles_deg_30 + angles_deg_45)))

angles_rad = [np.deg2rad(a) for a in angles_deg]
points_x = [np.cos(a) for a in angles_rad]
points_y = [np.sin(a) for a in angles_rad]

# --- Buat plot Unit Circle ---
theta = np.linspace(0, 2*np.pi, 360)
circle_x = np.cos(theta)
circle_y = np.sin(theta)

fig = go.Figure()

# Tambahkan warna kuadran
fig.add_shape(type="rect", x0=0, y0=0, x1=1.2, y1=1.2, fillcolor="rgba(227, 242, 253, 0.5)", line_width=0)  # Biru muda
fig.add_shape(type="rect", x0=-1.2, y0=0, x1=0, y1=1.2, fillcolor="rgba(232, 245, 233, 0.5)", line_width=0)  # Hijau muda
fig.add_shape(type="rect", x0=-1.2, y0=-1.2, x1=0, y1=0, fillcolor="rgba(255, 243, 224, 0.5)", line_width=0)  # Oranye muda
fig.add_shape(type="rect", x0=0, y0=-1.2, x1=1.2, y1=0, fillcolor="rgba(255, 235, 238, 0.5)", line_width=0)  # Merah muda

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
    hovertemplate="<b>%{text}</b><br>(%{x:.2f}, %{y:.2f})<extra></extra>",
    name="Sudut",
))

# Sumbu X dan Y
fig.add_shape(type="line", x0=-1.2, x1=1.2, y0=0, y1=0, line=dict(color="gray", width=1))
fig.add_shape(type="line", x0=0, x1=0, y0=-1.2, y1=1.2, line=dict(color="gray", width=1))

fig.update_layout(
    width=600, height=600,
    margin=dict(l=10, r=10, t=10, b=10),
    xaxis=dict(range=[-1.3, 1.3], visible=False),
    yaxis=dict(range=[-1.3, 1.3], visible=False),
    clickmode='event+select',
    showlegend=False,
    transition={'duration': 300, 'easing': 'linear-in-out'}  # Menambahkan animasi transisi
)

# --- Layout Aplikasi (2 kolom) ---
col1, col2 = st.columns([0.65, 0.35])

with col2:
    st.subheader("⚙️ Kontrol Sudut")
    # Input Angka
    st.number_input(
        "Masukkan sudut (derajat):", min_value=0, max_value=360,
        value=st.session_state.angle_deg, step=1,
        key='angle_num_input', on_change=update_angle
    )

    # Toggle untuk mode Radian
    st.toggle('Mode Radian', key='rad_mode', help="Tampilkan sudut dan nilai dalam radian.")

    st.markdown("---")
    
    # Slider untuk memilih sudut.
    st.slider(
        "Atau pilih dengan slider:", 0, 360,
        value=st.session_state.angle_deg, step=1, key="angle_slider", on_change=update_angle
    )

# --- Perhitungan dinamis berdasarkan state ---
angle_deg_current = st.session_state.angle_deg
angle_rad_selected = np.deg2rad(angle_deg_current)
x_point = np.cos(angle_rad_selected)
y_point = np.sin(angle_rad_selected)

# Tambahkan garis-garis dinamis ke objek 'fig' SEBELUM menampilkannya
# Garis Radius (Terminal) - Garis dari pusat ke titik di lingkaran
fig.add_trace(go.Scatter(x=[0, x_point], y=[0, y_point], mode="lines", line=dict(color="black", width=2), name="Radius", uid="radius"))
# Garis Sinus (merah) - Garis vertikal dari titik ke sumbu-x
fig.add_trace(go.Scatter(x=[x_point, x_point], y=[0, y_point], mode="lines", line=dict(color="red", width=3, dash='dash'), name="Sin", uid="sin_line"))
# Garis Cosinus (biru) - Garis horizontal dari pusat di sepanjang sumbu-x
fig.add_trace(go.Scatter(x=[0, x_point], y=[0, 0], mode="lines", line=dict(color="blue", width=3, dash='dash'), name="Cos", uid="cos_line"))

# Visualisasi untuk Tan dan Sec
if abs(x_point) > TOLERANCE:
    tan_val_selected = y_point / x_point
    tan_display_limit = 1.5
    tan_val_display = np.clip(tan_val_selected, -tan_display_limit, tan_display_limit)
    
    # Garis Tangen (hijau)
    fig.add_trace(go.Scatter(x=[1, 1], y=[0, tan_val_display], mode="lines", line=dict(color="green", width=3, dash='dash'), name="Tan", uid="tan_line"))
    # Garis Secant (ungu) - dari origin ke ujung garis tangen, membentuk hipotenusa
    fig.add_trace(go.Scatter(x=[0, 1], y=[0, tan_val_selected], mode="lines", line=dict(color="purple", width=2, dash='dot'), name="Sec", uid="sec_line"))

# Visualisasi untuk Cot dan Csc
if abs(y_point) > TOLERANCE:
    cot_val_selected = x_point / y_point
    cot_display_limit = 1.5
    cot_val_display = np.clip(cot_val_selected, -cot_display_limit, cot_display_limit)

    # Garis Cotangen (oranye) - garis singgung horizontal di (0,1)
    fig.add_trace(go.Scatter(x=[0, cot_val_display], y=[1, 1], mode="lines", line=dict(color="orange", width=3, dash='dash'), name="Cot", uid="cot_line"))
    # Garis Cosecan (pink) - dari origin ke ujung garis cotangen, membentuk hipotenusa
    fig.add_trace(go.Scatter(x=[0, cot_val_selected], y=[0, 1], mode="lines", line=dict(color="pink", width=2, dash='dot'), name="Csc", uid="csc_line"))

with col1:
    # --- Tampilkan Grafik Interaktif (HANYA SEKALI) --- 
    click_data = st.plotly_chart(fig, use_container_width=True, on_select="rerun", key="unit_circle")

# --- Hitung semua nilai trigonometri ---
angle_rad = np.deg2rad(angle_deg_current)
quadrant = get_quadrant(angle_deg_current % 360)
ref_angle = reference_angle(angle_deg_current)
sin_val = np.sin(angle_rad)
cos_val = np.cos(angle_rad)

tan_val = sin_val / cos_val if abs(cos_val) > TOLERANCE else "∞"
sec_val = 1 / cos_val if abs(cos_val) > TOLERANCE else "∞"
csc_val = 1 / sin_val if abs(sin_val) > TOLERANCE else "∞"
cot_val = cos_val / sin_val if abs(sin_val) > TOLERANCE else "∞"

with col2:
    # --- Info Sudut ---
    st.subheader("📘 Informasi Sudut")
    if st.session_state.rad_mode:
        st.markdown(f"**Sudut (θ):** `{angle_rad:.3f}` radian")
    else:
        st.markdown(f"**Sudut (θ):** `{angle_deg_current}°`")

    st.markdown(f"**Koordinat (x, y):** `({cos_val:.3f}, {sin_val:.3f})`")
    st.markdown(f"**Kuadran:** {quadrant}")
    if not st.session_state.rad_mode:
        st.markdown(f"**Sudut Relasi:** {ref_angle}°")

    st.subheader("🔢 Nilai Fungsi")
    m1, m2 = st.columns(2)
    m3, m4 = st.columns(2)
    m5, m6 = st.columns(2)
    
    m1.metric(label="sin(θ)", value=f"{sin_val:.3f}" if isinstance(sin_val, float) else sin_val)
    m2.metric(label="cos(θ)", value=f"{cos_val:.3f}" if isinstance(cos_val, float) else cos_val)
    m3.metric(label="tan(θ)", value=f"{tan_val:.3f}" if isinstance(tan_val, float) else tan_val)
    m4.metric(label="cot(θ)", value=f"{cot_val:.3f}" if isinstance(cot_val, float) else cot_val)
    m5.metric(label="csc(θ)", value=f"{csc_val:.3f}" if isinstance(csc_val, float) else csc_val)
    m6.metric(label="sec(θ)", value=f"{sec_val:.3f}" if isinstance(sec_val, float) else sec_val)

    st.markdown("<br>", unsafe_allow_html=True) # Spacer
    st.subheader("💡 Identitas Pythagoras")
    pythagorean_eq = f"`sin²θ + cos²θ = ({sin_val:.3f})² + ({cos_val:.3f})²`"
    pythagorean_res = f"`= {sin_val**2:.3f} + {cos_val**2:.3f} = {sin_val**2 + cos_val**2:.1f}`"
    st.markdown(pythagorean_eq)
    st.markdown(pythagorean_res)

st.markdown("---")
st.caption("Dikembangkan untuk membantu siswa memahami konsep sudut dan relasinya pada Unit Circle 🌐")
