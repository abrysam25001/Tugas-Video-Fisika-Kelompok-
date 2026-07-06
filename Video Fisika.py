import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Simulasi Video Fisika", layout="wide")

st.title("🎬 Dashboard Video Simulasi Fisika Interaktif")
st.write("Ubah parameter di kiri, lalu klik tombol **▶ PLAY** di bagian bawah grafik untuk memutar simulasi!")

# Navigasi Materi
materi = st.sidebar.selectbox(
    "Pilih Materi Video:",
    [
        "1. Gelombang Berjalan",
        "2. Gerak Parabola (Proyektil)",
        "3. Energi Kinetik & Potensial",
        "4. Hukum Archimedes",
        "5. Dinamika Fluida (Pipa)",
        "6. Gerak di Bidang Miring",
        "7. Gerak Harmonik Sederhana (Pegas)"
    ]
)

st.sidebar.markdown("---")

# Fungsi pembantu untuk membuat layout animasi yang seragam
def get_animation_layout(title_text, x_range, y_range, show_axes=True):
    return go.Layout(
        title=title_text,
        xaxis=dict(range=x_range, autorange=False, visible=show_axes),
        yaxis=dict(range=y_range, autorange=False, visible=show_axes),
        height=550,
        updatemenus=[dict(
            type="buttons",
            direction="left",
            pad={"r": 10, "t": 87},
            showactive=False,
            x=0.1, y=0, xanchor="right", yanchor="top",
            buttons=[
                dict(label="▶ PLAY", method="animate",
                     args=[None, dict(frame=dict(duration=50, redraw=True), transition=dict(duration=0), fromcurrent=True, mode="immediate")]),
                dict(label="⏸ PAUSE", method="animate",
                     args=[[None], dict(frame=dict(duration=0, redraw=False), mode="immediate", transition=dict(duration=0))])
            ]
        )]
    )

# ------------------------------------------------------------------
# 1. GELOMBANG BERJALAN (Peselancar 🏄‍♂️)
# ------------------------------------------------------------------
if materi == "1. Gelombang Berjalan":
    st.header("🌊 Simulasi Gelombang (Peselancar)")
    
    amp = st.sidebar.slider("Amplitudo (Tinggi Ombak)", 0.5, 4.0, 2.0, 0.1)
    freq = st.sidebar.slider("Frekuensi (Kecepatan Gelombang)", 0.5, 3.0, 1.0, 0.1)
    lam = st.sidebar.slider("Panjang Gelombang (λ)", 2.0, 10.0, 5.0, 0.5)
    
    x = np.linspace(0, 20, 300)
    k = (2 * np.pi) / lam
    omega = 2 * np.pi * freq
    
    t_vals = np.linspace(0, 5, 80)
    
    # Kondisi Awal (t=0)
    y_init = amp * np.sin(omega * 0 - k * x)
    x_surf = 10
    y_surf = amp * np.sin(omega * 0 - k * x_surf)
    
    fig = go.Figure(
        data=[
            go.Scatter(x=x, y=y_init, mode='lines', line=dict(color='#00BFFF', width=6), name="Air"),
            go.Scatter(x=[x_surf], y=[y_surf + 0.5], mode='text', text="🏄‍♂️", textfont=dict(size=45), name="Peselancar")
        ],
        layout=get_animation_layout("Gelombang Air Bergerak", [0, 20], [-5, 5]),
        frames=[
            go.Frame(
                data=[
                    go.Scatter(x=x, y=(amp * np.sin(omega * t - k * x))),
                    go.Scatter(x=[x_surf], y=[(amp * np.sin(omega * t - k * x_surf)) + 0.5])
                ],
                traces=[0, 1]
            ) for t in t_vals
        ]
    )
    st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------------------------------
# 2. GERAK PARABOLA (Roket Terbang 🚀)
# ------------------------------------------------------------------
elif materi == "2. Gerak Parabola (Proyektil)":
    st.header("🚀 Simulasi Lintasan Parabola (Roket)")
    
    v0 = st.sidebar.slider("Kecepatan Peluncuran (v0)", 10, 50, 30)
    alpha = st.sidebar.slider("Sudut Peluncuran (°)", 15, 90, 45)
    g = 9.8
    
    rad = np.radians(alpha)
    t_total = (2 * v0 * np.sin(rad)) / g
    
    t_vals = np.linspace(0, t_total, 60)
    x_all = v0 * np.cos(rad) * t_vals
    y_all = (v0 * np.sin(rad) * t_vals) - (0.5 * g * t_vals**2)
    
    fig = go.Figure(
        data=[
            go.Scatter(x=x_all, y=y_all, mode='lines', line=dict(dash='dot', color='gray'), name="Jalur"),
            go.Scatter(x=[x_all[0]], y=[y_all[0]], mode='text', text="🚀", textfont=dict(size=40), name="Roket")
        ],
        layout=get_animation_layout("Peluncuran Roket Melengkung", [0, max(x_all)+10], [0, max(y_all)+10]),
        frames=[
            go.Frame(data=[go.Scatter(x=[x_all[i]], y=[y_all[i]])], traces=[1])
            for i in range(len(t_vals))
        ]
    )
    st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------------------------------
# 3. ENERGI KINETIK & POTENSIAL (Ikan Paus 🐳 Jatuh)
# ------------------------------------------------------------------
elif materi == "3. Energi Kinetik & Potensial":
    st.header("🐳 Simulasi Konservasi Energi (Ikan Paus Jatuh)")
    
    massa = st.sidebar.slider("Massa Paus (ton)", 1, 10, 5)
    h_awal = st.sidebar.slider("Ketinggian Helikopter (m)", 10, 100, 50)
    
    g = 9.8
    t_total = np.sqrt((2 * h_awal) / g)
    t_vals = np.linspace(0, t_total, 60)
    
    # Supaya skalanya seimbang di grafik, kita normalisasi energinya menjadi ketinggian (h_awal = 100% Energi Total)
    fig = go.Figure(
        data=[
            # Bar Energi Potensial (EP)
            go.Bar(x=['Energi Potensial'], y=[h_awal], marker_color='#005088', width=0.4, name="EP"),
            # Bar Energi Kinetik (EK)
            go.Bar(x=['Energi Kinetik'], y=[0], marker_color='#11caa0', width=0.4, name="EK"),
            # Objek Paus
            go.Scatter(x=['Paus Jatuh'], y=[h_awal], mode='text', text="🐳", textfont=dict(size=60), name="Paus")
        ],
        layout=get_animation_layout("Ikan Paus Terjun Bebas & Grafik Energi", [-0.5, 2.5], [0, h_awal + 10]),
        frames=[
            go.Frame(
                data=[
                    go.Bar(y=[max(0, h_awal - (0.5 * g * t**2))]), # Tinggi EP menyusut
                    go.Bar(y=[h_awal - max(0, h_awal - (0.5 * g * t**2))]), # Tinggi EK membesar
                    go.Scatter(y=[max(0, h_awal - (0.5 * g * t**2))]) # Paus ikut turun
                ],
                traces=[0, 1, 2]
            ) for t in t_vals
        ]
    )
    st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------------------------------
# 4. HUKUM ARCHIMEDES (Bebek Karet 🦆)
# ------------------------------------------------------------------
elif materi == "4. Hukum Archimedes":
    st.header("🦆 Simulasi Gaya Apung (Bebek Karet Nyemplung)")
    
    rho_cair = st.sidebar.slider("Massa Jenis Cairan (kg/m³)", 600, 1400, 1000)
    rho_benda = st.sidebar.slider("Massa Jenis Bebek (kg/m³)", 200, 1800, 700)
    
    if rho_benda < rho_cair:
        y_final = (rho_benda / rho_cair) * 1.5 - 1.0
    elif rho_benda == rho_cair:
        y_final = -1.0
    else:
        y_final = -2.5
        
    y_vals = np.linspace(2.5, y_final, 40)
    
    fig = go.Figure(
        data=[
            # Air
            go.Scatter(x=[0, 4, 4, 0], y=[0, 0, -3, -3], fill='toself', fillcolor='rgba(0,191,255,0.4)', mode='none', name="Air"),
            # Bebek Karet
            go.Scatter(x=[2], y=[2.5], mode='text', text="🦆", textfont=dict(size=70), name="Bebek")
        ],
        layout=get_animation_layout("Posisi Benda di dalam Fluida", [0, 4], [-3, 4], show_axes=False),
        frames=[
            go.Frame(data=[go.Scatter(x=[2], y=[y])], traces=[1])
            for y in y_vals
        ]
    )
    st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------------------------------
# 5. DINAMIKA FLUIDA (Kawanan Ikan 🐟)
# ------------------------------------------------------------------
elif materi == "5. Dinamika Fluida (Pipa)":
    st.header("🐟 Simulasi Aliran Pipa (Kecepatan Ikan)")
    
    r1 = st.sidebar.slider("Radius Pipa Besar Masuk", 5.0, 10.0, 8.0)
    r2 = st.sidebar.slider("Radius Pipa Kecil Keluar", 2.0, 5.0, 3.0)
    
    # Gambar Pipa sebagai bentuk background (shapes)
    shapes = [
        dict(type="line", x0=0, y0=r1, x1=3, y1=r1, line=dict(width=4)),
        dict(type="line", x0=0, y0=-r1, x1=3, y1=-r1, line=dict(width=4)),
        dict(type="line", x0=3, y0=r1, x1=5, y1=r2, line=dict(width=4)),
        dict(type="line", x0=3, y0=-r1, x1=5, y1=-r2, line=dict(width=4)),
        dict(type="line", x0=5, y0=r2, x1=9, y1=r2, line=dict(width=4)),
        dict(type="line", x0=5, y0=-r2, x1=9, y1=-r2, line=dict(width=4))
    ]
    
    v1 = 1.0 
    v2 = ((r1**2) * v1) / (r2**2) # Persamaan kontinuitas
    
    frames_data = []
    x_ikan = np.array([0.0, 0.8, 1.6]) # Posisi awal 3 ikan
    
    for _ in range(70):
        # Hitung posisi baru tiap ikan berdasarkan kecepatan di pipa
        for i in range(3):
            if x_ikan[i] < 4.0:
                x_ikan[i] += v1 * 0.1
            else:
                x_ikan[i] += v2 * 0.1
            
            if x_ikan[i] > 9:
                x_ikan[i] = -0.5
                
        frames_data.append(list(x_ikan))
        
    layout = get_animation_layout("Kecepatan Ikan di Pipa Menyempit", [0, 9], [-15, 15], show_axes=False)
    layout.shapes = shapes
    
    fig = go.Figure(
        data=[go.Scatter(x=frames_data[0], y=[0, 0, 0], mode='text', text=["🐟", "🐟", "🐟"], textfont=dict(size=45))],
        layout=layout,
        frames=[go.Frame(data=[go.Scatter(x=pos, y=[0, 0, 0])], traces=[0]) for pos in frames_data]
    )
    st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------------------------------
# 6. GERAK DI BIDANG MIRING (Penguin Meluncur 🐧)
# ------------------------------------------------------------------
elif materi == "6. Gerak di Bidang Miring":
    st.header("🐧 Simulasi Bidang Miring (Penguin Main Es)")
    
    theta = st.sidebar.slider("Sudut Kemiringan Es (°)", 10, 60, 30)
    rad = np.radians(theta)
    g = 9.8
    accel = g * np.sin(rad)
    
    L = 10.0 # Panjang sisi miring es
    t_total = np.sqrt((2 * L) / accel)
    t_vals = np.linspace(0, t_total, 50)
    
    # Koordinat segitiga Es yang benar dan rapi
    x_es = [0, L * np.cos(rad), L * np.cos(rad), 0]
    y_es = [L * np.sin(rad), L * np.sin(rad), 0, L * np.sin(rad)] # Perbaikan bentuk segitiga kanan
    
    fig = go.Figure(
        data=[
            # Gunung Es (Segitiga Sempurna)
            go.Scatter(x=[0, L*np.cos(rad), 0, 0], y=[0, 0, L*np.sin(rad), 0], fill="toself", fillcolor="#B0E0E6", mode="lines", line=dict(color="blue", width=3), name="Es"),
            # Penguin
            go.Scatter(x=[0], y=[L * np.sin(rad) + 0.5], mode='text', text="🐧", textfont=dict(size=50), name="Penguin")
        ],
        layout=get_animation_layout("Penguin Meluncur Turun", [-1, L+1], [-1, L+2], show_axes=False),
        frames=[
            go.Frame(
                data=[
                    go.Scatter(x=[(0.5 * accel * t**2) * np.cos(rad)], 
                               y=[(L - (0.5 * accel * t**2)) * np.sin(rad) + 0.5])
                ],
                traces=[1]
            ) for t in t_vals
        ]
    )
    st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------------------------------
# 7. GERAK HARMONIK SEDERHANA (Monyet Bouncing 🐒)
# ------------------------------------------------------------------
elif materi == "7. Gerak Harmonik Sederhana (Pegas)":
    st.header("🐒 Simulasi Osilasi Pegas (Monyet Berayun)")
    
    k_pegas = st.sidebar.slider("Konstanta Pegas (k)", 20, 100, 50)
    m_beban = st.sidebar.slider("Massa Monyet (m)", 0.5, 4.0, 2.0)
    
    omega = np.sqrt(k_pegas / m_beban)
    t_vals = np.linspace(0, 6, 80)
    
    fig = go.Figure(
        data=[
            # Batas Atap
            go.Scatter(x=[1.5, 2.5], y=[5, 5], mode='lines', line=dict(color="black", width=6), name="Atap"),
            # Tali/Pegas
            go.Scatter(x=[2, 2], y=[5, 3.5], mode='lines', line=dict(color="purple", width=4, dash='dot'), name="Pegas"),
            # Monyet
            go.Scatter(x=[2], y=[3.5], mode='text', text="🐒", textfont=dict(size=70), name="Monyet")
        ],
        layout=get_animation_layout("Simpangan Harmonik Monyet", [1, 3], [-1, 6], show_axes=False),
        frames=[
            go.Frame(
                data=[
                    go.Scatter(x=[1.5, 2.5], y=[5, 5]), # Atap Tetap
                    go.Scatter(x=[2, 2], y=[5, 3.5 + 2.0 * np.cos(omega * t)]), # Pegas Memanjang/Memendek
                    go.Scatter(x=[2], y=[3.5 + 2.0 * np.cos(omega * t) - 0.2])   # Monyet ikut pegas
                ],
                traces=[0, 1, 2]
            ) for t in t_vals
        ]
    )
    st.plotly_chart(fig, use_container_width=True)