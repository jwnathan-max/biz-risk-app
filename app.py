import streamlit as st
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# -----------------------------------------------------------
# [이메일 발송 설정]
# -----------------------------------------------------------
# 보안을 위해 Streamlit Secrets 기능으로 이메일과 비밀번호를 숨겨서 불러옵니다.
SENDER_EMAIL = st.secrets["SENDER_EMAIL"]
SENDER_PASSWORD = st.secrets["SENDER_PASSWORD"]
RECEIVER_EMAIL = st.secrets["RECEIVER_EMAIL"]
# -----------------------------------------------------------

def send_db_email(name, phone, company, score, corp, cap, gaji, surp, strat):
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = f"🚨 [신규 DB 접수] {name} 대표님 - 법인 리스크 {score}점"

        body = f"""
        대표님, 새로운 법인 리스크 진단 DB가 접수되었습니다! 즉시 확인 후 연락해 보세요.

        [고객 기본 정보]
        👤 성함/직급: {name}
        🏢 기업명: {company if company else '미입력'}
        📞 연락처: {phone}
        ⚠️ 종합 리스크 점수: {score}점

        [상세 진단 내역]
        1. 회사 형태: {corp}
        2. 자본금 규모: {cap}
        3. 가지급금 규모: {gaji}
        4. 미처분이익잉여금: {surp}
        5. 신자본환원 등 실행 여부: {strat}
        
        * 본 DB는 '개인정보 수집 및 이용'에 동의한 합법적인 영업 활용 가능 데이터입니다.
        """
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        text = msg.as_string()
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, text)
        server.quit()
        return True
    except Exception as e:
        # 이메일 발송 실패 시 콘솔에 에러 출력 (고객 화면에는 정상 처리된 것처럼 보임)
        print(f"이메일 발송 실패: {e}")
        return False

# 1. 페이지 기본 설정
st.set_page_config(page_title="우리 법인 리스크 1분 진단", page_icon="🏢", layout="centered")

# CSS 스타일링
st.markdown("""
    <style>
    .main-title { font-size: 42px; font-weight: 900; color: #0A1931; margin-bottom: 5px; line-height: 1.2; word-break: keep-all; letter-spacing: -1px; }
    .sub-title { font-size: 18px; color: #4a5068; margin-bottom: 35px; line-height: 1.5; word-break: keep-all; }
    .highlight { color: #C9A84C; font-weight: bold; }
    .stButton>button { background-color: #0A1931; color: white; font-weight: bold; font-size: 18px; width: 100%; padding: 15px; border-radius: 5px; }
    .stButton>button:hover { background-color: #C9A84C; color: #0A1931; border-color: #C9A84C; }
    .privacy-text { font-size: 12px; color: #666; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">우리 법인 리스크 1분 진단</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">장부 속 숨은 시한폭탄을 확인하고, <span class="highlight"></span>의 맞춤형 절세 리포트를 받아보세요.</p>', unsafe_allow_html=True)

# 2. 진단 폼 시작
with st.form("risk_form"):
    st.write("### Q1. 현재 대표님 회사의 형태는 무엇입니까?")
    corp_type = st.radio("회사 형태", ["법인 사업자", "개인 사업자 (성실신고 대상 포함)"], label_visibility="collapsed")
    
    st.write("---")
    st.write("### Q2. 현재 법인의 '자본금' 규모는 어느 정도입니까?")
    capital = st.radio("자본금 규모", ["1억 원 미만", "1억 원 ~ 3억 원", "3억 원 이상"], label_visibility="collapsed")

    st.write("---")
    st.write("### Q3. 법인 내에 '가지급금'이 쌓여 있습니까?")
    gajigeup = st.radio("가지급금 규모", ["1억 원 미만", "1억 원 ~ 3억 원", "3억 원 이상"], label_visibility="collapsed")
    
    st.write("---")
    st.write("### Q4. '미처분이익잉여금' 규모는 어느 정도입니까?")
    surplus = st.radio("미처분이익잉여금 규모", ["3억 원 미만", "3억 원 ~ 10억 원", "10억 원 이상"], label_visibility="collapsed")
    
    st.write("---")
    st.write("### Q5. 최근 3년 내에 '신이익소각' 등 자본 구조 개선을 실행하신 적이 있습니까?")
    strategy = st.radio("재무 전략 실행 여부", ["예, 컨설팅을 통해 실행했습니다.", "아니오, 들어본 적 없거나 고민만 하고 있습니다."], label_visibility="collapsed")

    st.write("---")
    st.write("### 🎁 [진단 결과 및 무료 절세 리포트 수령]")
    
    col1, col2 = st.columns(2)
    with col1:
        user_name = st.text_input("성함 (직급) *필수")
    with col2:
        user_phone = st.text_input("연락처 (결과 수신용) *필수")
        
    company_name = st.text_input("기업명 (선택)")

    # 개인정보 동의 체크박스 추가
    st.write("---")
    privacy_agree = st.checkbox("개인정보 수집 및 이용 동의 (필수)")
    st.markdown('<p class="privacy-text">* 수집항목: 성명, 연락처, 기업명 및 재무응답 데이터<br>* 수집목적: 진단 결과 리포트 발송 및 맞춤형 1:1 컨설팅 상담<br>* 보유기간: 상담 종료 후 6개월 보관 뒤 즉시 파기</p>', unsafe_allow_html=True)

    submit_button = st.form_submit_button("🚨 리스크 점수 확인 및 리포트 신청하기")

# 3. 결과 산출 및 클로징 로직
if submit_button:
    if not privacy_agree:
        st.error("🔒 개인정보 수집 및 이용에 동의해 주셔야 진단 결과를 확인하실 수 있습니다.")
    elif not user_name or not user_phone:
        st.error("성함과 연락처를 모두 입력해 주셔야 정확한 진단 리포트를 발송해 드릴 수 있습니다.")
    else:
        with st.spinner("대표님의 재무 데이터를 분석 중입니다..."):
            time.sleep(1.5)
            
        st.success("분석이 완료되었습니다!")
        
        # 리스크 점수 계산 초기화 (100점 만점 체계)
        risk_score = 0
        if corp_type == "개인 사업자 (성실신고 대상 포함)": risk_score += 10
        
        cap_tier = 0
        if "1억 원 미만" in capital: 
            risk_score += 10
            cap_tier = 0
        elif "1억 원 ~ 3억 원" in capital: 
            risk_score += 5
            cap_tier = 1
        elif "3억 원 이상" in capital: 
            risk_score += 0
            cap_tier = 2

        gaji_tier = 0
        if "3억 원 이상" in gajigeup: 
            risk_score += 45
            gaji_tier = 2
        elif "1억 원 ~ 3억 원" in gajigeup: 
            risk_score += 25
            gaji_tier = 1
        elif "1억 원 미만" in gajigeup: 
            risk_score += 10
            gaji_tier = 0
        
        surp_tier = 0
        if "10억 원 이상" in surplus: 
            risk_score += 25
            surp_tier = 2
        elif "3억 원 ~ 10억 원" in surplus: 
            risk_score += 15
            surp_tier = 1
        elif "3억 원 미만" in surplus: 
            risk_score += 5
            surp_tier = 0
        
        if "아니오" in strategy: risk_score += 10
        
        # 백그라운드에서 대표님 이메일로 DB 발송 실행
        send_db_email(user_name, user_phone, company_name, risk_score, corp_type, capital, gajigeup, surplus, strategy)

        # 결과 출력
        st.write("---")
        st.markdown(f"### ⚠️ {user_name} 대표님의 현재 재무/세무 리스크는 **{risk_score}점** 입니다.")
        
        if risk_score >= 60:
            st.error("**[위험 단계] 막대한 인정이자와 세금 폭탄 리스크에 노출되어 있습니다.** 당장 합법적인 가지급금 정리 플랜이 필요합니다.")
            if gaji_tier > 0:
                if cap_tier < gaji_tier:
                    st.warning(f"🚨 **[자본금 한도 초과 경고]** 대표님, 현재 잉여금이 충분하시더라도 **'자본금 한도' 제약 때문에 액면가 취득으로 가지급금을 한 번에 전액 상계할 수 없습니다.** 남은 가지급금을 안전하게 소거하려면 이익소각 등 **2~3가지 복합 병합 플랜이 반드시 필요**합니다.")
                elif surp_tier < gaji_tier:
                    st.warning(f"🚨 **[잉여금 부족 경고]** 가지급금 규모 대비 이를 상계할 **미처분이익잉여금(배당재원)이 부족**합니다. 엑시트 전략 병행이 시급합니다.")
                else:
                    st.info("💡 **[VIP 솔루션 매칭]** 대표님! 현재 보유하신 자본금과 잉여금의 사이즈가 완벽합니다. **세금 부담 없이 가지급금을 전액 상계할 수 있는 '신자본환원' 솔루션** 적용이 바로 가능한 최상의 조건입니다. 절대 개인 자산으로 갚지 마시고 즉시 연락 주십시오.")
                    
        elif risk_score >= 35:
            st.warning("**[주의 단계] 이익잉여금과 가지급금이 누적되며 기업 가치를 훼손하고 있습니다.** 잉여금 엑시트(Exit) 컨설팅을 통한 정리가 시급합니다.")
        else:
            st.success("**[양호 단계] 기본 관리가 되고 있습니다.** 다만, 향후 성장을 대비해 절세를 극대화할 수 있는 추가 설계가 필요합니다.")
            
        st.write("---")
        st.write("💡 입력하신 연락처로 **이규원 전략기획 팀장**이 직접 분석한 상세 절세 솔루션을 곧 보내드리겠습니다.")
        st.markdown("**📞 Direct: 010-8977-7768 / 070-8098-2060**")