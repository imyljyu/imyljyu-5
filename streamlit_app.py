import streamlit as st
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots

st.set_page_config(layout="wide", page_title="3D 공간좌표 교구")
st.title("📐 3D 공간좌표 시각화 교구")
st.write("고등학교 기하 공간좌표 단원을 위한 대화형 학습 교구입니다.")

# 세션 상태 초기화
if 'original_point' not in st.session_state:
    st.session_state.original_point = None
if 'current_point' not in st.session_state:
    st.session_state.current_point = None
if 'projection_plane' not in st.session_state:
    st.session_state.projection_plane = None
if 'symmetry_type' not in st.session_state:
    st.session_state.symmetry_type = None

# 좌표 입력 섹션
st.header("점의 좌표 입력")
col1, col2, col3, col4 = st.columns(4)
with col1:
    x = st.number_input("x", value=0, step=1, key="x_input", format="%d")
with col2:
    y = st.number_input("y", value=0, step=1, key="y_input", format="%d")
with col3:
    z = st.number_input("z", value=0, step=1, key="z_input", format="%d")
with col4:
    st.write("")
    st.write("")
    if st.button("입력", key="input_btn", use_container_width=True):
        st.session_state.original_point = np.array([int(x), int(y), int(z)])
        st.session_state.current_point = np.array([int(x), int(y), int(z)])
        st.session_state.projection_plane = None
        st.session_state.symmetry_type = None
        st.success(f"점 ({int(x)}, {int(y)}, {int(z)})이 입력되었습니다!")

if st.session_state.original_point is not None:
    # 3D 시각화 함수
    def create_3d_plot(current_point, original_point, projection_plane=None, symmetry_type=None):
        fig = go.Figure()
        
        # 축 그리기 (범위: -10 ~ 10)
        axis_range = 10
        
        # x축 (빨강)
        fig.add_trace(go.Scatter3d(
            x=[0, axis_range], y=[0, 0], z=[0, 0],
            mode='lines', name='x축',
            line=dict(color='red', width=2)
        ))
        
        # y축 (초록)
        fig.add_trace(go.Scatter3d(
            x=[0, 0], y=[0, axis_range], z=[0, 0],
            mode='lines', name='y축',
            line=dict(color='green', width=2)
        ))
        
        # z축 (파랑)
        fig.add_trace(go.Scatter3d(
            x=[0, 0], y=[0, 0], z=[0, axis_range],
            mode='lines', name='z축',
            line=dict(color='blue', width=2)
        ))
        
        # 원래 점
        fig.add_trace(go.Scatter3d(
            x=[original_point[0]], y=[original_point[1]], z=[original_point[2]],
            mode='markers+text', name='입력 점',
            marker=dict(size=10, color='black'),
            text=[f'({int(original_point[0])}, {int(original_point[1])}, {int(original_point[2])})'],
            textposition='top center'
        ))
        
        # 현재 점
        if current_point is not None:
            fig.add_trace(go.Scatter3d(
                x=[current_point[0]], y=[current_point[1]], z=[current_point[2]],
                mode='markers+text', name='변환 점',
                marker=dict(size=12, color='orange'),
                text=[f'({int(current_point[0])}, {int(current_point[1])}, {int(current_point[2])})'],
                textposition='bottom center'
            ))
        
        # 평면 표시
        if projection_plane == 'xy':
            # xy 평면에 내린 수선
            projection = np.array([current_point[0], current_point[1], 0])
            fig.add_trace(go.Scatter3d(
                x=[current_point[0], projection[0]], 
                y=[current_point[1], projection[1]], 
                z=[current_point[2], projection[2]],
                mode='lines', name='수선',
                line=dict(color='orange', width=3, dash='dash')
            ))
            fig.add_trace(go.Scatter3d(
                x=[projection[0]], y=[projection[1]], z=[projection[2]],
                mode='markers+text', name='xy평면 수선의 발',
                marker=dict(size=10, color='orange'),
                text=[f'({int(projection[0])}, {int(projection[1])}, 0)'],
                textposition='top center'
            ))
        
        elif projection_plane == 'yz':
            # yz 평면에 내린 수선
            projection = np.array([0, current_point[1], current_point[2]])
            fig.add_trace(go.Scatter3d(
                x=[current_point[0], projection[0]], 
                y=[current_point[1], projection[1]], 
                z=[current_point[2], projection[2]],
                mode='lines', name='수선',
                line=dict(color='orange', width=3, dash='dash')
            ))
            fig.add_trace(go.Scatter3d(
                x=[projection[0]], y=[projection[1]], z=[projection[2]],
                mode='markers+text', name='yz평면 수선의 발',
                marker=dict(size=10, color='orange'),
                text=[f'(0, {int(projection[1])}, {int(projection[2])})'],
                textposition='top center'
            ))
        
        elif projection_plane == 'zx':
            # zx 평면에 내린 수선
            projection = np.array([current_point[0], 0, current_point[2]])
            fig.add_trace(go.Scatter3d(
                x=[current_point[0], projection[0]], 
                y=[current_point[1], projection[1]], 
                z=[current_point[2], projection[2]],
                mode='lines', name='수선',
                line=dict(color='orange', width=3, dash='dash')
            ))
            fig.add_trace(go.Scatter3d(
                x=[projection[0]], y=[projection[1]], z=[projection[2]],
                mode='markers+text', name='zx평면 수선의 발',
                marker=dict(size=10, color='orange'),
                text=[f'({int(projection[0])}, 0, {int(projection[2])})'],
                textposition='top center'
            ))
        
        # 좌표평면 표시 (반투명)
        opacity = 0.1
        
        # xy 평면
        xy_plane_x = [-axis_range, axis_range, axis_range, -axis_range]
        xy_plane_y = [-axis_range, -axis_range, axis_range, axis_range]
        xy_plane_z = [0, 0, 0, 0]
        fig.add_trace(go.Surface(
            x=[-axis_range, axis_range],
            y=[-axis_range, axis_range],
            z=[[0, 0], [0, 0]],
            opacity=opacity, colorscale='Reds', showscale=False, name='xy평면'
        ))
        
        # yz 평면
        fig.add_trace(go.Surface(
            x=[[0, 0], [0, 0]],
            y=[-axis_range, axis_range],
            z=[-axis_range, axis_range],
            opacity=opacity, colorscale='Greens', showscale=False, name='yz평면'
        ))
        
        # zx 평면
        fig.add_trace(go.Surface(
            x=[-axis_range, axis_range],
            y=[[0, 0], [0, 0]],
            z=[-axis_range, axis_range],
            opacity=opacity, colorscale='Blues', showscale=False, name='zx평면'
        ))
        
        fig.update_layout(
            title=f"3D 공간좌표 시각화",
            scene=dict(
                xaxis_title='x',
                yaxis_title='y',
                zaxis_title='z',
                xaxis=dict(backgroundcolor='rgba(200,200,200,0.2)', gridcolor='gray'),
                yaxis=dict(backgroundcolor='rgba(200,200,200,0.2)', gridcolor='gray'),
                zaxis=dict(backgroundcolor='rgba(200,200,200,0.2)', gridcolor='gray'),
                xaxis_range=[-axis_range, axis_range],
                yaxis_range=[-axis_range, axis_range],
                zaxis_range=[-axis_range, axis_range]
            ),
            width=1000,
            height=800,
            showlegend=True
        )
        
        return fig
    
    # 탭 섹션
    tab1, tab2 = st.tabs(["🎯 수선의 발", "🔄 대칭이동"])
    
    with tab1:
        st.header("평면에 내린 수선의 발")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("xy평면에 투영", use_container_width=True, key="xy_proj"):
                st.session_state.projection_plane = 'xy'
                st.session_state.symmetry_type = None
                st.rerun()
        
        with col2:
            if st.button("yz평면에 투영", use_container_width=True, key="yz_proj"):
                st.session_state.projection_plane = 'yz'
                st.session_state.symmetry_type = None
                st.rerun()
        
        with col3:
            if st.button("zx평면에 투영", use_container_width=True, key="zx_proj"):
                st.session_state.projection_plane = 'zx'
                st.session_state.symmetry_type = None
                st.rerun()
    
    with tab2:
        st.header("점의 대칭이동")
        
        st.subheader("평면에 대한 대칭이동")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("xy평면 대칭", use_container_width=True, key="xy_sym"):
                st.session_state.current_point = np.array([
                    st.session_state.original_point[0],
                    st.session_state.original_point[1],
                    -st.session_state.original_point[2]
                ])
                st.session_state.symmetry_type = 'xy평면'
                st.session_state.projection_plane = None
                st.rerun()
        
        with col2:
            if st.button("yz평면 대칭", use_container_width=True, key="yz_sym"):
                st.session_state.current_point = np.array([
                    -st.session_state.original_point[0],
                    st.session_state.original_point[1],
                    st.session_state.original_point[2]
                ])
                st.session_state.symmetry_type = 'yz평면'
                st.session_state.projection_plane = None
                st.rerun()
        
        with col3:
            if st.button("zx평면 대칭", use_container_width=True, key="zx_sym"):
                st.session_state.current_point = np.array([
                    st.session_state.original_point[0],
                    -st.session_state.original_point[1],
                    st.session_state.original_point[2]
                ])
                st.session_state.symmetry_type = 'zx평면'
                st.session_state.projection_plane = None
                st.rerun()
        
        st.subheader("축에 대한 대칭이동")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("x축 대칭", use_container_width=True, key="x_sym"):
                st.session_state.current_point = np.array([
                    st.session_state.original_point[0],
                    -st.session_state.original_point[1],
                    -st.session_state.original_point[2]
                ])
                st.session_state.symmetry_type = 'x축'
                st.session_state.projection_plane = None
                st.rerun()
        
        with col2:
            if st.button("y축 대칭", use_container_width=True, key="y_sym"):
                st.session_state.current_point = np.array([
                    -st.session_state.original_point[0],
                    st.session_state.original_point[1],
                    -st.session_state.original_point[2]
                ])
                st.session_state.symmetry_type = 'y축'
                st.session_state.projection_plane = None
                st.rerun()
        
        with col3:
            if st.button("z축 대칭", use_container_width=True, key="z_sym"):
                st.session_state.current_point = np.array([
                    -st.session_state.original_point[0],
                    -st.session_state.original_point[1],
                    st.session_state.original_point[2]
                ])
                st.session_state.symmetry_type = 'z축'
                st.session_state.projection_plane = None
                st.rerun()
        
        st.subheader("원점에 대한 대칭")
        if st.button("원점 대칭", use_container_width=True, key="origin_sym"):
            st.session_state.current_point = -st.session_state.original_point
            st.session_state.symmetry_type = '원점'
            st.session_state.projection_plane = None
            st.rerun()
    
    st.divider()
    
    # 3D 그래프 표시
    fig = create_3d_plot(
        st.session_state.current_point,
        st.session_state.original_point,
        st.session_state.projection_plane,
        st.session_state.symmetry_type
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # 좌표 정보 표시
    st.header("좌표 정보")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("입력 점")
        st.write(f"({int(st.session_state.original_point[0])}, {int(st.session_state.original_point[1])}, {int(st.session_state.original_point[2])})")
    
    with col2:
        st.subheader("변환 점")
        st.write(f"({int(st.session_state.current_point[0])}, {int(st.session_state.current_point[1])}, {int(st.session_state.current_point[2])})")
    
    if st.session_state.projection_plane:
        st.info(f"📌 {st.session_state.projection_plane}에 내린 수선의 발을 보여줍니다.")
    elif st.session_state.symmetry_type:
        st.info(f"📌 {st.session_state.symmetry_type}에 대한 대칭이동을 보여줍니다.")
    
    col1, col2 = st.columns(2)
    with col1:
        pass
    with col2:
        if st.button("초기화", use_container_width=True, key="reset"):
            st.session_state.original_point = None
            st.session_state.current_point = None
            st.session_state.projection_plane = None
            st.session_state.symmetry_type = None
            st.rerun()
else:
    st.info("🔢 위의 x, y, z에 숫자를 입력하고 '입력' 버튼을 클릭하세요!")
