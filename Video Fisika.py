import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Simulasi Video Fisika", layout="wide")

st.title("🎬 Dashboard Video Simulasi Fisika Interaktif")
st.write("Atur parameter, lalu klik tombol **▶ PLAY** pada grafik di bawah untuk memutar simulasi video!")

# Navigasi Materi di Sidebar
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

# Profil Seluruh Anggota Kelompok di Sidebar (Format Seragam)
st.sidebar.markdown("### 👨‍💻 Anggota Kelompok")
st.sidebar.write("1. **Ziandara Rasendrya** (230210250003)")
st.sidebar.write("2. **Helvina Ariella S. P** (230210250012)")
st.sidebar.write("3. **Alya Kayyisah Santoso** (230210250015)")
st.sidebar.write("4. **Hafzahtu Zuhri** (230210250019)")
st.sidebar.write("5. **Heavenly Jibrilliant L.** (230210250023)")
st.sidebar.write("6. **Abrysam Ariffa'iq** (230210250030)")
st.sidebar.write("7. **Jaelani Azzamil P. R.** (230210250042)")

st.sidebar.markdown("---")

def get_animation_layout(title_text, x_range, y_range, show_axes=True):
    return go.Layout(
        title=dict(text=title_text, font=dict(color='#00FFFF', size=20)),
        xaxis=dict(range=x_range, autorange=False, visible=show_axes, gridcolor='#333333', zerolinecolor='#555555'),
        yaxis=dict(range=y_range, autorange=False, visible=show_axes, gridcolor='#333333', zerolinecolor='#555555'),
        height=550,
        template="plotly_dark",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        updatemenus=[dict(
            type="buttons",
            direction="left",
            pad={"r": 10, "t": 87},
            showactive=False,
            x=0.1, y=0, xanchor="right", yanchor="top",
            font=dict(color="white"),
            bgcolor="#FF4B4B",
            buttons=[
                dict(label="▶ PLAY", method="animate",
                     args=[None, dict(frame=dict(duration=50, redraw=True), transition=dict(duration=0), fromcurrent=True, mode="immediate")]),
                dict(label="⏸ PAUSE", method="animate",
                     args=[[None], dict(frame=dict(duration=0, redraw=False), mode="immediate", transition=dict(duration=0))])
            ]
        )]
    )

# ==================================================================
# 1. GELOMBANG BERJALAN 
# ==================================================================
if materi == "1. Gelombang Berjalan":
    st.header("🌊 Simulasi Gelombang (Peselancar)")
    
    c_anim = st.container()
    c_info = st.container()
    c_param = st.container()
    c_rumus = st.container()
    
    with c_param:
        st.markdown("### ⚙️ Parameter:")
        amp = st.slider("Amplitudo (Tinggi Ombak)", 0.5, 4.0, 2.0, 0.1)
        freq = st.slider("Frekuensi (f)", 0.5, 3.0, 1.0, 0.1)
        lam = st.slider("Panjang Gelombang (λ)", 2.0, 10.0, 5.0, 0.5)
    
    # Hitungan Info
    cepat_rambat = lam * freq
    periode = 1 / freq
    
    x = np.linspace(0, 20, 300)
    k = (2 * np.pi) / lam
    omega = 2 * np.pi * freq
    t_vals = np.linspace(0, 5, 80)
    
    y_init = amp * np.sin(omega * 0 - k * x)
    x_surf = 10
    
    with c_anim:
        fig = go.Figure(
            data=[
                go.Scatter(x=x, y=y_init, mode='lines', line=dict(color='#00FFFF', width=6), name="Air"),
                go.Scatter(x=[x_surf], y=[(amp * np.sin(omega * 0 - k * x_surf)) + 0.5], mode='text', text="🏄‍♂️", textfont=dict(size=45), name="Peselancar")
            ],
            layout=get_animation_layout("Gelombang Air Bergerak", [0, 20], [-5, 5]),
            frames=[go.Frame(data=[go.Scatter(x=x, y=(amp * np.sin(omega * t - k * x))), go.Scatter(x=[x_surf], y=[(amp * np.sin(omega * t - k * x_surf)) + 0.5])], traces=[0, 1]) for t in t_vals]
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with c_info:
        st.markdown(f"""
        <div style="background-color: #1E1E1E; border-left: 5px solid #00FFFF; padding: 15px; border-radius: 8px; margin-bottom: 12px;">
            <p style="margin: 0; font-size: 14px; color: #AAAAAA;">Cepat Rambat (v)</p>
            <h3 style="margin: 5px 0 0 0; color: #FFFFFF;">{cepat_rambat:.2f} m/s</h3>
        </div>
        <div style="background-color: #1E1E1E; border-left: 5px solid #39FF14; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
            <p style="margin: 0; font-size: 14px; color: #AAAAAA;">Periode (T)</p>
            <h3 style="margin: 5px 0 0 0; color: #FFFFFF;">{periode:.2f} s</h3>
        </div>
        """, unsafe_allow_html=True)

    with c_rumus:
        st.write("**Rumus Gelombang Berjalan:**")
        st.latex(r"y = A \sin(\omega t - kx)")
        st.latex(r"v = \lambda \cdot f")

# ==================================================================
# 2. GERAK PARABOLA 
# ==================================================================
elif materi == "2. Gerak Parabola (Proyektil)":
    st.header("🚀 Simulasi Lintasan Parabola (Roket)")
    
    c_anim = st.container()
    c_info = st.container()
    c_param = st.container()
    c_rumus = st.container()
    
    with c_param:
        st.markdown("### ⚙️ Parameter:")
        v0 = st.slider("Kecepatan Peluncuran (v0)", 10, 50, 30)
        alpha = st.slider("Sudut Peluncuran (°)", 15, 90, 45)
        
    g = 9.8
    rad = np.radians(alpha)
    t_total = (2 * v0 * np.sin(rad)) / g
    x_maks = (v0**2 * np.sin(2*rad)) / g
    y_maks = (v0**2 * (np.sin(rad)**2)) / (2*g)
    
    t_vals = np.linspace(0, t_total, 60)
    x_all = v0 * np.cos(rad) * t_vals
    y_all = (v0 * np.sin(rad) * t_vals) - (0.5 * g * t_vals**2)
    
    with c_anim:
        fig = go.Figure(
            data=[
                go.Scatter(x=x_all, y=y_all, mode='lines', line=dict(dash='dot', color='#FFFF00', width=3), name="Jalur"),
                go.Scatter(x=[x_all[0]], y=[y_all[0]], mode='text', text="🚀", textfont=dict(size=40), name="Roket")
            ],
            layout=get_animation_layout("Peluncuran Roket Melengkung", [0, max(x_all)+10], [0, max(y_all)+10]),
            frames=[go.Frame(data=[go.Scatter(x=[x_all[i]], y=[y_all[i]])], traces=[1]) for i in range(len(t_vals))]
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with c_info:
        st.markdown(f"""
        <div style="background-color: #1E1E1E; border-left: 5px solid #FFFF00; padding: 15px; border-radius: 8px; margin-bottom: 12px;">
            <p style="margin: 0; font-size: 14px; color: #AAAAAA;">Jarak Maksimum (X maks)</p>
            <h3 style="margin: 5px 0 0 0; color: #FFFFFF;">{x_maks:.2f} m</h3>
        </div>
        <div style="background-color: #1E1E1E; border-left: 5px solid #00FFFF; padding: 15px; border-radius: 8px; margin-bottom: 12px;">
            <p style="margin: 0; font-size: 14px; color: #AAAAAA;">Ketinggian Maksimum (Y maks)</p>
            <h3 style="margin: 5px 0 0 0; color: #FFFFFF;">{y_maks:.2f} m</h3>
        </div>
        <div style="background-color: #1E1E1E; border-left: 5px solid #FF00FF; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
            <p style="margin: 0; font-size: 14px; color: #AAAAAA;">Waktu Udara (t total)</p>
            <h3 style="margin: 5px 0 0 0; color: #FFFFFF;">{t_total:.2f} s</h3>
        </div>
        """, unsafe_allow_html=True)

    with c_rumus:
        st.write("**Rumus Gerak Parabola:**")
        st.latex(r"X_{maks} = \frac{v_0^2 \sin(2\alpha)}{g}")
        st.latex(r"Y_{maks} = \frac{v_0^2 \sin^2(\alpha)}{2g}")

# ==================================================================
# 3. ENERGI KINETIK & POTENSIAL 
# ==================================================================
elif materi == "3. Energi Kinetik & Potensial":
    st.header("🐳 Simulasi Konservasi Energi")
    
    c_anim = st.container()
    c_info = st.container()
    c_param = st.container()
    c_rumus = st.container()
    
    with c_param:
        st.markdown("### ⚙️ Parameter:")
        massa = st.slider("Massa Paus (ton)", 1, 10, 5)
        h_awal = st.slider("Ketinggian Awal (m)", 10, 100, 50)
        
    g = 9.8
    massa_kg = massa * 1000
    ep_awal = massa_kg * g * h_awal
    v_akhir = np.sqrt(2 * g * h_awal)
    
    t_total = np.sqrt((2 * h_awal) / g)
    t_vals = np.linspace(0, t_total, 60)
    
    with c_anim:
        fig = go.Figure(
            data=[
                go.Bar(x=['Energi Potensial'], y=[h_awal], marker_color='#FF00FF', width=0.4, name="EP"),
                go.Bar(x=['Energi Kinetik'], y=[0], marker_color='#39FF14', width=0.4, name="EK"),
                go.Scatter(x=['Paus Jatuh'], y=[h_awal], mode='text', text="🐳", textfont=dict(size=60), name="Paus")
            ],
            layout=get_animation_layout("Paus Terjun Bebas & Grafik Energi", [-0.5, 2.5], [0, h_awal + 10]),
            frames=[go.Frame(data=[go.Bar(y=[max(0, h_awal - (0.5 * g * t**2))]), go.Bar(y=[h_awal - max(0, h_awal - (0.5 * g * t**2))]), go.Scatter(y=[max(0, h_awal - (0.5 * g * t**2))])], traces=[0, 1, 2]) for t in t_vals]
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with c_info:
        st.markdown(f"""
        <div style="background-color: #1E1E1E; border-left: 5px solid #FF00FF; padding: 15px; border-radius: 8px; margin-bottom: 12px;">
            <p style="margin: 0; font-size: 14px; color: #AAAAAA;">Total Energi Mekanik (Joule)</p>
            <h3 style="margin: 5px 0 0 0; color: #FFFFFF;">{ep_awal:,.0f} J</h3>
        </div>
        <div style="background-color: #1E1E1E; border-left: 5px solid #39FF14; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
            <p style="margin: 0; font-size: 14px; color: #AAAAAA;">Kecepatan Jatuh Maksimal (v)</p>
            <h3 style="margin: 5px 0 0 0; color: #FFFFFF;">{v_akhir:.2f} m/s</h3>
        </div>
        """, unsafe_allow_html=True)

    with c_rumus:
        st.write("**Rumus Energi Mekanik (EM = EP + EK):**")
        st.latex(r"EM = mgh + \frac{1}{2}mv^2")
        st.latex(r"v = \sqrt{2gh}")

# ==================================================================
# 4. HUKUM ARCHIMEDES 
# ==================================================================
elif materi == "4. Hukum Archimedes":
    st.header("🦆 Simulasi Gaya Apung")
    
    c_anim = st.container()
    c_info = st.container()
    c_param = st.container()
    c_rumus = st.container()
    
    with c_param:
        st.markdown("### ⚙️ Parameter:")
        rho_cair = st.slider("Massa Jenis Cairan (kg/m³)", 600, 1400, 1000)
        rho_benda = st.slider("Massa Jenis Bebek (kg/m³)", 200, 1800, 700)
        
    if rho_benda < rho_cair:
        y_final = (rho_benda / rho_cair) * 1.5 - 1.0
        status = "TERAPUNG"
        warna_status = "#39FF14"
    elif rho_benda == rho_cair:
        y_final = -1.0
        status = "MELAYANG"
        warna_status = "#FFFF00"
    else:
        y_final = -2.5
        status = "TENGGELAM"
        warna_status = "#FF4B4B"
        
    y_vals = np.linspace(2.5, y_final, 40)
    
    with c_anim:
        fig = go.Figure(
            data=[
                go.Scatter(x=[0, 4, 4, 0], y=[0, 0, -3, -3], fill='toself', fillcolor='rgba(0, 255, 255, 0.3)', line=dict(color='#00FFFF'), mode='lines', name="Air"),
                go.Scatter(x=[2], y=[2.5], mode='text', text="🦆", textfont=dict(size=70), name="Bebek")
            ],
            layout=get_animation_layout("Posisi Benda di dalam Fluida", [0, 4], [-3, 4], show_axes=False),
            frames=[go.Frame(data=[go.Scatter(x=[2], y=[y])], traces=[1]) for y in y_vals]
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with c_info:
        st.markdown(f"""
        <div style="background-color: #1E1E1E; border-left: 5px solid {warna_status}; padding: 15px; border-radius: 8px; margin-bottom: 12px;">
            <p style="margin: 0; font-size: 14px; color: #AAAAAA;">Rasio Massa Jenis (ρ_benda / ρ_cairan)</p>
            <h3 style="margin: 5px 0 0 0; color: #FFFFFF;">{(rho_benda/rho_cair):.2f}</h3>
        </div>
        <div style="background-color: #1E1E1E; border-left: 5px solid {warna_status}; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
            <p style="margin: 0; font-size: 14px; color: #AAAAAA;">Status Benda</p>
            <h3 style="margin: 5px 0 0 0; color: {warna_status};">{status}</h3>
        </div>
        """, unsafe_allow_html=True)

    with c_rumus:
        st.write("**Rumus Gaya Apung (Archimedes):**")
        st.latex(r"F_a = \rho_{\text{cair}} \cdot g \cdot V_{\text{celup}}")

# ==================================================================
# 5. DINAMIKA FLUIDA 
# ==================================================================
elif materi == "5. Dinamika Fluida (Pipa)":
    st.header("🐟 Simulasi Aliran Pipa")
    
    c_anim = st.container()
    c_info = st.container()
    c_param = st.container()
    c_rumus = st.container()
    
    with c_param:
        st.markdown("### ⚙️ Parameter:")
        r1 = st.slider("Radius Pipa Besar Masuk", 5.0, 10.0, 8.0)
        r2 = st.slider("Radius Pipa Kecil Keluar", 2.0, 5.0, 3.0)
        
    v1 = 1.0 
    A1 = np.pi * (r1**2)
    A2 = np.pi * (r2**2)
    v2 = (A1 * v1) / A2
    
    shapes = [
        dict(type="line", x0=0, y0=r1, x1=3, y1=r1, line=dict(color='#FFFFFF', width=4)), 
        dict(type="line", x0=0, y0=-r1, x1=3, y1=-r1, line=dict(color='#FFFFFF', width=4)),
        dict(type="line", x0=3, y0=r1, x1=5, y1=r2, line=dict(color='#FFFFFF', width=4)),
        dict(type="line", x0=3, y0=-r1, x1=5, y1=-r2, line=dict(color='#FFFFFF', width=4)),
        dict(type="line", x0=5, y0=r2, x1=9, y1=r2, line=dict(color='#FFFFFF', width=4)),
        dict(type="line", x0=5, y0=-r2, x1=9, y1=-r2, line=dict(color='#FFFFFF', width=4))
    ]
    
    frames_data = []
    x_ikan = np.array([0.0, 0.8, 1.6])
    for _ in range(70):
        for i in range(3):
            if x_ikan[i] < 4.0:
                x_ikan[i] += v1 * 0.1
            else:
                x_ikan[i] += v2 * 0.1
            if x_ikan[i] > 9:
                x_ikan[i] = -0.5
        frames_data.append(list(x_ikan))
        
    with c_anim:
        layout = get_animation_layout("Kecepatan Ikan di Pipa Menyempit", [0, 9], [-15, 15], show_axes=False)
        layout.shapes = shapes
        fig = go.Figure(
            data=[go.Scatter(x=frames_data[0], y=[0, 0, 0], mode='text', text=["🐟", "🐟", "🐟"], textfont=dict(size=45))],
            layout=layout,
            frames=[go.Frame(data=[go.Scatter(x=pos, y=[0, 0, 0])], traces=[0]) for pos in frames_data]
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with c_info:
        st.markdown(f"""
        <div style="background-color: #1E1E1E; border-left: 5px solid #00FFFF; padding: 15px; border-radius: 8px; margin-bottom: 12px;">
            <p style="margin: 0; font-size: 14px; color: #AAAAAA;">Luas Penampang Masuk (A1) vs Keluar (A2)</p>
            <h3 style="margin: 5px 0 0 0; color: #FFFFFF;">{A1:.1f} m² vs {A2:.1f} m²</h3>
        </div>
        <div style="background-color: #1E1E1E; border-left: 5px solid #FF00FF; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
            <p style="margin: 0; font-size: 14px; color: #AAAAAA;">Kecepatan Alir Keluar (v2)</p>
            <h3 style="margin: 5px 0 0 0; color: #FFFFFF;">{v2:.2f} m/s</h3>
        </div>
        """, unsafe_allow_html=True)

    with c_rumus:
        st.write("**Rumus Persamaan Kontinuitas:**")
        st.latex(r"A_1 \cdot v_1 = A_2 \cdot v_2")

# ==================================================================
# 6. GERAK DI BIDANG MIRING 
# ==================================================================
elif materi == "6. Gerak di Bidang Miring":
    st.header("🐧 Simulasi Bidang Miring")
    
    c_anim = st.container()
    c_info = st.container()
    c_param = st.container()
    c_rumus = st.container()
    
    with c_param:
        st.markdown("### ⚙️ Parameter:")
        theta = st.slider("Sudut Kemiringan (θ)", 10, 60, 30)
        mu = st.slider("Koefisien Gesek (μ)", 0.0, 1.0, 0.30, step=0.01)
        m = st.slider("Massa Penguin (kg)", 1.0, 10.0, 5.0)
        
    g = 9.8
    rad = np.radians(theta)
    w_x = m * g * np.sin(rad)
    f_max = mu * m * g * np.cos(rad)
    
    if w_x > f_max:
        accel = (w_x - f_max) / m
        status = "Bergerak Meluncur"
        status_color = "#39FF14" 
    else:
        accel = 0.0
        status = "Diam"
        status_color = "#FF4B4B" 
        
    with c_anim:
        L = 10.0 
        if accel > 0:
            t_total = np.sqrt((2 * L) / accel)
            t_vals = np.linspace(0, t_total, 50)
        else:
            t_total = 0
            t_vals = [0]
            
        fig = go.Figure(
            data=[
                go.Scatter(x=[0, L*np.cos(rad), 0, 0], y=[0, 0, L*np.sin(rad), 0], fill="toself", fillcolor="rgba(0, 255, 255, 0.2)", mode="lines", line=dict(color="#00FFFF", width=3), name="Es"),
                go.Scatter(x=[0], y=[L * np.sin(rad) + 0.5], mode='text', text="🐧", textfont=dict(size=50), name="Penguin")
            ],
            layout=get_animation_layout("Penguin Meluncur Turun", [-1, L+1], [-1, L+2], show_axes=False)
        )
        
        frames = []
        for t in t_vals:
            if accel > 0:
                x_p = (0.5 * accel * t**2) * np.cos(rad)
                y_p = (L - (0.5 * accel * t**2)) * np.sin(rad) + 0.5
            else:
                x_p = 0
                y_p = L * np.sin(rad) + 0.5
            frames.append(go.Frame(data=[go.Scatter(x=[x_p], y=[y_p])], traces=[1]))
            
        fig.frames = frames
        st.plotly_chart(fig, use_container_width=True)

    with c_info:
        st.markdown(f"""
        <div style="background-color: #1E1E1E; border-left: 5px solid #00FFFF; padding: 15px; border-radius: 8px; margin-bottom: 12px;">
            <p style="margin: 0; font-size: 14px; color: #AAAAAA;">Gaya Penggerak (mg sin θ)</p>
            <h3 style="margin: 5px 0 0 0; color: #FFFFFF;">{w_x:.2f} N</h3>
        </div>
        <div style="background-color: #1E1E1E; border-left: 5px solid #FFFF00; padding: 15px; border-radius: 8px; margin-bottom: 12px;">
            <p style="margin: 0; font-size: 14px; color: #AAAAAA;">Gaya Gesek Maks (f_gesek)</p>
            <h3 style="margin: 5px 0 0 0; color: #FFFFFF;">{f_max:.2f} N</h3>
        </div>
        <div style="background-color: #1E1E1E; border-left: 5px solid {status_color}; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
            <p style="margin: 0; font-size: 14px; color: #AAAAAA;">Percepatan (a) | Status</p>
            <h3 style="margin: 5px 0 0 0; color: {status_color};">{accel:.2f} m/s² | {status}</h3>
        </div>
        """, unsafe_allow_html=True)
        
    with c_rumus:
        st.write("**Rumus Percepatan (Dengan Gesekan):**")
        st.latex(r"a = \frac{mg \sin \theta - \mu mg \cos \theta}{m}")

# ==================================================================
# 7. GERAK HARMONIK SEDERHANA
# ==================================================================
elif materi == "7. Gerak Harmonik Sederhana (Pegas)":
    st.header("🐒 Simulasi Osilasi Pegas")
    
    c_anim = st.container()
    c_info = st.container()
    c_param = st.container()
    c_rumus = st.container()
    
    with c_param:
        st.markdown("### ⚙️ Parameter:")
        k_pegas = st.slider("Konstanta Pegas (k)", 20, 100, 50)
        m_beban = st.slider("Massa Monyet (m)", 0.5, 4.0, 2.0)
        
    omega = np.sqrt(k_pegas / m_beban)
    periode = (2 * np.pi) / omega
    t_vals = np.linspace(0, 6, 80)
    
    with c_anim:
        fig = go.Figure(
            data=[
                go.Scatter(x=[1.5, 2.5], y=[5, 5], mode='lines', line=dict(color="#FFFFFF", width=6), name="Atap"),
                go.Scatter(x=[2, 2], y=[5, 3.5], mode='lines', line=dict(color="#FF00FF", width=4, dash='dot'), name="Pegas"),
                go.Scatter(x=[2], y=[3.5], mode='text', text="🐒", textfont=dict(size=70), name="Monyet")
            ],
            layout=get_animation_layout("Simpangan Harmonik Monyet", [1, 3], [-1, 6], show_axes=False),
            frames=[go.Frame(data=[go.Scatter(x=[1.5, 2.5], y=[5, 5]), go.Scatter(x=[2, 2], y=[5, 3.5 + 2.0 * np.cos(omega * t)]), go.Scatter(x=[2], y=[3.5 + 2.0 * np.cos(omega * t) - 0.2])], traces=[0, 1, 2]) for t in t_vals]
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with c_info:
        st.markdown(f"""
        <div style="background-color: #1E1E1E; border-left: 5px solid #FF00FF; padding: 15px; border-radius: 8px; margin-bottom: 12px;">
            <p style="margin: 0; font-size: 14px; color: #AAAAAA;">Frekuensi Sudut (ω)</p>
            <h3 style="margin: 5px 0 0 0; color: #FFFFFF;">{omega:.2f} rad/s</h3>
        </div>
        <div style="background-color: #1E1E1E; border-left: 5px solid #39FF14; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
            <p style="margin: 0; font-size: 14px; color: #AAAAAA;">Periode Osilasi (T)</p>
            <h3 style="margin: 5px 0 0 0; color: #FFFFFF;">{periode:.2f} s</h3>
        </div>
        """, unsafe_allow_html=True)

    with c_rumus:
        st.write("**Rumus Frekuensi Sudut & Simpangan:**")
        st.latex(r"\omega = \sqrt{\frac{k}{m}} \quad \text{dan} \quad y = A \cos(\omega t)")
