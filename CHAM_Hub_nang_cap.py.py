import streamlit as st
import pandas as pd
import plotly.express as px
import random
from datetime import datetime

# ============================================================
# CHẠM HUB — BẢN NÂNG CẤP GIAO DIỆN & TƯƠNG TÁC
# Prototype Streamlit. Dữ liệu nhật ký/bức tường hiện lưu trong
# session_state của từng phiên, chưa phải hệ thống đa người dùng.
# ============================================================

st.set_page_config(
    page_title="CHẠM Hub | Thấu hiểu để kết nối",
    page_icon="🪷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------- DESIGN SYSTEM ---------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@300;400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Be Vietnam Pro', sans-serif; }
.stApp { background: #F5F7F6; color: #18324A; }
[data-testid="stSidebar"] { background: #18324A; }
[data-testid="stSidebar"] * { color: #F7FAF8 !important; }
.hero {
  padding: 2.1rem 2.2rem; border-radius: 24px; color: white;
  background: linear-gradient(120deg,#18324A 0%,#28566A 55%,#2D6A4F 100%);
  margin-bottom: 1.2rem; position: relative; overflow: hidden;
}
.hero h1 { color: white; font-size: clamp(2rem,4vw,3.2rem); margin:0; font-weight:800; }
.hero p { color:#E7F2EC; font-size:1.05rem; margin:.5rem 0 0 0; }
.eyebrow { color:#F2C66D; letter-spacing:.16em; font-weight:700; font-size:.78rem; }
.panel {
  background:white; padding:1.15rem 1.25rem; border-radius:18px;
  border:1px solid #E5ECE8; box-shadow:0 7px 22px rgba(24,50,74,.045);
  margin-bottom:.8rem;
}
.panel h3 { margin-top:0; color:#18324A; }
.soft { color:#61736C; font-size:.92rem; }
.pill { display:inline-block; padding:.28rem .7rem; border-radius:999px;
  background:#E4F1EA; color:#27634C; font-size:.78rem; font-weight:700; }
.quote {
  padding:1rem 1.2rem; border-left:5px solid #D18A55; border-radius:12px;
  background:#FFF6ED; color:#65472F; font-style:italic;
}
.step {
  border-radius:15px; background:#EAF2F5; padding:1rem; height:100%;
  border:1px solid #DCE8ED;
}
div[data-testid="stMetric"] {
  background:white; border:1px solid #E5ECE8; padding:14px 16px;
  border-radius:16px;
}
.stButton button { border-radius:12px; font-weight:700; min-height:2.7rem; }
hr { border-color:#E5ECE8; }
footer {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# --------------------------- DATA ---------------------------
CARD_DECK = [
    {"code":"KT-01","group":"Kiến thức","title":"Quên thông thường và dấu hiệu cần lưu ý",
     "scenario":"Một người thường xuyên quên những việc vừa xảy ra và gặp khó khăn khi thực hiện công việc quen thuộc.",
     "task":"Theo bạn, gia đình nên làm gì?",
     "choices":["A. Kết luận ngay người đó mắc Alzheimer.","B. Theo dõi biểu hiện, trao đổi với người thân và khuyến khích đi khám chuyên môn.","C. Bỏ qua vì ai lớn tuổi cũng sẽ như vậy."],
     "answer":1,"why":"Không thể tự chẩn đoán Alzheimer qua một biểu hiện đơn lẻ. Suy giảm trí nhớ ảnh hưởng sinh hoạt cần được nhân viên y tế đánh giá."},
    {"code":"KT-02","group":"Kiến thức","title":"Alzheimer ảnh hưởng đến điều gì?",
     "scenario":"Một bạn hỏi Alzheimer có chỉ ảnh hưởng đến trí nhớ hay không.",
     "task":"Chọn nhận định phù hợp nhất.",
     "choices":["A. Chỉ ảnh hưởng khả năng ghi nhớ.","B. Có thể ảnh hưởng trí nhớ, tư duy, ngôn ngữ và sinh hoạt hằng ngày.","C. Chỉ ảnh hưởng thể chất."],
     "answer":1,"why":"Alzheimer là bệnh tiến triển ảnh hưởng nhiều chức năng nhận thức, không chỉ riêng trí nhớ."},
    {"code":"GN-01","group":"Góc nhìn","title":"Câu hỏi được lặp lại",
     "scenario":"Bà hỏi bạn lần thứ tư: “Mấy giờ mẹ con về?”.",
     "task":"Cách phản hồi nào thể hiện sự tôn trọng?",
     "choices":["A. “Con trả lời rồi mà!”","B. Nhẹ nhàng trả lời lại, có thể viết giờ về ở nơi dễ nhìn.","C. Im lặng bỏ đi."],
     "answer":1,"why":"Trả lời bình tĩnh và dùng gợi ý trực quan có thể giúp người bệnh bớt lo lắng."},
    {"code":"GN-02","group":"Góc nhìn","title":"Khi người thân cảm thấy bối rối",
     "scenario":"Ông không nhận ra một món đồ quen thuộc và tỏ ra xấu hổ.",
     "task":"Bạn nên làm gì?",
     "choices":["A. Trêu đùa để ông vui.","B. Bình tĩnh hỗ trợ, tránh làm ông mất mặt trước người khác.","C. Nói rằng ông không còn tự làm được gì."],
     "answer":1,"why":"Giữ phẩm giá và tránh làm người bệnh xấu hổ là nguyên tắc quan trọng trong giao tiếp."},
    {"code":"NC-01","group":"Nghiên cứu","title":"Kiểm chứng thông tin",
     "scenario":"Nhóm tìm thấy một bài đăng mạng xã hội khẳng định có cách chữa khỏi Alzheimer.",
     "task":"Bước phù hợp nhất là gì?",
     "choices":["A. Chia sẻ ngay để nhiều người biết.","B. Kiểm tra nguồn y tế đáng tin cậy và không xem bài đăng là kết luận khoa học.","C. Đưa vào trò chơi nếu bài viết có nhiều lượt thích."],
     "answer":1,"why":"Thông tin sức khỏe cần được đối chiếu với nguồn chuyên môn đáng tin cậy."},
    {"code":"CN-01","group":"Công nghệ","title":"Công cụ nhắc lịch",
     "scenario":"Gia đình muốn hỗ trợ người thân nhớ lịch sinh hoạt hằng ngày.",
     "task":"Giải pháp nào có thể cân nhắc?",
     "choices":["A. Lịch trực quan hoặc lời nhắc đơn giản, phù hợp với khả năng của người sử dụng.","B. Cài ứng dụng phức tạp mà không hướng dẫn.","C. Công khai lịch và thông tin cá nhân lên mạng."],
     "answer":0,"why":"Công nghệ nên dễ sử dụng, phù hợp nhu cầu và bảo vệ quyền riêng tư."},
    {"code":"CS-01","group":"Chăm sóc – Cộng đồng","title":"Hỗ trợ khi người thân lo lắng",
     "scenario":"Mẹ có vẻ lo lắng khi không tìm thấy chiếc ví.",
     "task":"Bạn nên bắt đầu thế nào?",
     "choices":["A. Tranh cãi rằng mẹ đãng trí.","B. Thừa nhận cảm xúc lo lắng và bình tĩnh cùng tìm ở những nơi quen thuộc.","C. Giấu chuyện để mẹ khỏi hỏi."],
     "answer":1,"why":"Lắng nghe cảm xúc và hỗ trợ tìm kiếm thường hữu ích hơn tranh cãi đúng sai."},
    {"code":"HT-01","group":"Hợp tác","title":"Một khu phố quan tâm",
     "scenario":"Một nhóm học sinh muốn xây dựng hoạt động nâng cao nhận thức tại khu dân cư.",
     "task":"Việc nào nên được ưu tiên?",
     "choices":["A. Tự ý công bố thông tin của một gia đình có người mắc bệnh.","B. Phối hợp với nhà trường, gia đình và đơn vị phù hợp; xin phép trước khi chia sẻ câu chuyện.","C. Tổ chức hoạt động mà không cần kiểm chứng nội dung."],
     "answer":1,"why":"Hoạt động cộng đồng cần tôn trọng quyền riêng tư, có sự đồng thuận và sử dụng thông tin chính xác."},
    {"code":"TC-01","group":"Thử thách","title":"Từ chối tắm",
     "scenario":"Người thân từ chối tắm và có vẻ sợ hãi.",
     "task":"Bạn sẽ thử cách nào trước?",
     "choices":["A. Ép buộc ngay lập tức.","B. Tìm hiểu điều khiến họ khó chịu, chọn thời điểm phù hợp và giải thích từng bước nhẹ nhàng.","C. Quát mắng để họ nghe lời."],
     "answer":1,"why":"Tìm nguyên nhân gây khó chịu, bảo đảm riêng tư và điều chỉnh cách hỗ trợ có thể giảm căng thẳng."},
    {"code":"TG-01","group":"Thời gian – Sự kiện","title":"Ngày hội nhận thức",
     "scenario":"Trường tổ chức ngày hội tìm hiểu về Alzheimer.",
     "task":"Thông điệp nào phù hợp với tinh thần CHẠM?",
     "choices":["A. Người mắc bệnh không còn khả năng đóng góp.","B. Mỗi người đều xứng đáng được tôn trọng, lắng nghe và hỗ trợ.","C. Gia đình phải tự giải quyết mọi khó khăn."],
     "answer":1,"why":"CHẠM hướng đến thấu hiểu, kết nối và thúc đẩy sự tham gia của cộng đồng."}
]

GUIDES = [
    {"name":"Lặp lại câu hỏi","tag":"Giao tiếp","problem":"Người thân hỏi cùng một câu nhiều lần trong thời gian ngắn.",
     "avoid":"Trách móc, quát mắng hoặc cố chứng minh rằng họ đã được trả lời.",
     "try":"Trả lời ngắn gọn, bình tĩnh; dùng lịch, đồng hồ hoặc ghi chú dễ nhìn; thử chuyển sang hoạt động quen thuộc nếu phù hợp.",
     "note":"Nếu thay đổi hành vi xuất hiện đột ngột hoặc đi kèm dấu hiệu bất thường, gia đình nên tìm tư vấn y tế."},
    {"name":"Lo lắng vì thất lạc đồ","tag":"Cảm xúc","problem":"Người thân tin rằng ai đó đã lấy đồ của mình.",
     "avoid":"Đôi co, chế giễu hoặc buộc tội ngược lại.",
     "try":"Lắng nghe cảm xúc, trấn an và cùng tìm ở những nơi thường đặt đồ. Có thể bố trí một vị trí cất đồ cố định.",
     "note":"Nếu tình trạng nghi ngờ gây nguy hiểm hoặc căng thẳng kéo dài, nên trao đổi với nhân viên y tế."},
    {"name":"Bối rối vào chiều tối","tag":"An toàn","problem":"Người thân trở nên bồn chồn hoặc mất định hướng vào cuối ngày.",
     "avoid":"Quát mắng, bỏ mặc hoặc sử dụng biện pháp khóa nhốt gây nguy hiểm.",
     "try":"Giữ lịch sinh hoạt đều đặn, giảm tiếng ồn, bảo đảm ánh sáng và kiểm tra các nguy cơ mất an toàn trong nhà.",
     "note":"Cần có kế hoạch an toàn phù hợp với từng người; không áp dụng một biện pháp khóa cửa cho mọi gia đình."},
    {"name":"Từ chối tắm rửa","tag":"Sinh hoạt","problem":"Người thân từ chối tắm hoặc trở nên căng thẳng khi được hỗ trợ.",
     "avoid":"Ép buộc, kéo giật hoặc làm người đó xấu hổ.",
     "try":"Tìm hiểu nguyên nhân như lạnh, sợ trượt ngã, thiếu riêng tư; chuẩn bị trước vật dụng và hướng dẫn từng bước.",
     "note":"Nếu có đau, khó nuốt, sụt cân hoặc vấn đề sức khỏe khác, cần xin tư vấn chuyên môn."}
]

SOURCES = [
    ("WHO — Dementia","https://www.who.int/news-room/fact-sheets/detail/dementia"),
    ("NIA — Alzheimer’s Symptoms and Diagnosis","https://www.nia.nih.gov/health/alzheimers-symptoms-and-diagnosis"),
    ("CDC — Signs and Symptoms of Alzheimer’s","https://www.cdc.gov/alzheimers-dementia/signs-symptoms/alzheimers.html"),
    ("NHS — Communicating with Someone with Dementia","https://www.nhs.uk/conditions/dementia/living-with-dementia/communication/"),
    ("NIA — Alzheimer’s Caregiving","https://www.nia.nih.gov/health/alzheimers-caregiving"),
    ("WHO — Dementia-Friendly Initiatives Toolkit","https://www.who.int/publications/i/item/9789240031531"),
    ("ADI — Dementia Friendly Communities","https://www.alzint.org/what-we-do/policy/dementia-friendly-communities/"),
    ("ADI — World Alzheimer Report 2024","https://www.alzint.org/resource/world-alzheimer-report-2024/")
]

# --------------------------- SESSION STATE ---------------------------
defaults = {
    "visited": False, "drawn_card": None, "quiz_score": 0,
    "quiz_done": [], "journal": [], "wall": [], "guide_feedback": {}
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# --------------------------- SIDEBAR ---------------------------
with st.sidebar:
    st.markdown("<div style='text-align:center;font-size:3rem'>🪷</div>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center;color:white'>CHẠM HUB</h2>", unsafe_allow_html=True)
    st.caption("THẤU HIỂU ĐỂ KẾT NỐI")
    st.divider()
    page = st.radio(
        "KHÔNG GIAN TRẢI NGHIỆM",
        ["🏠 Trang chủ","📊 Hiểu về Alzheimer","🧭 Cẩm nang đồng hành",
         "🎲 Trạm trải nghiệm","💌 Không gian sẻ chia","📚 Nguồn tham khảo"],
        label_visibility="visible"
    )
    st.divider()
    st.markdown("**Thông điệp CHẠM**")
    st.markdown("*Không ai phải đi một mình.*")
    st.caption("Phiên bản trải nghiệm — nội dung giáo dục, không thay thế tư vấn y tế.")

def hero(kicker, title, subtitle):
    st.markdown(f"""
    <div class="hero">
      <div class="eyebrow">{kicker}</div>
      <h1>{title}</h1>
      <p>{subtitle}</p>
    </div>""", unsafe_allow_html=True)

def panel(title, body):
    st.markdown(f'<div class="panel"><h3>{title}</h3>{body}</div>', unsafe_allow_html=True)

# --------------------------- HOME ---------------------------
if page == "🏠 Trang chủ":
    hero("MỘT HÀNH TRÌNH THẤU HIỂU", "CHẠM — Không ai phải đi một mình",
         "Một không gian giáo dục tương tác giúp chúng ta hiểu hơn về Alzheimer, học cách đồng hành và kết nối cộng đồng.")
    st.markdown('<div class="quote">“Có thể ký ức đổi thay, nhưng mỗi người vẫn luôn cần được lắng nghe, tôn trọng và yêu thương.”</div>', unsafe_allow_html=True)
    a,b,c = st.columns(3)
    a.metric("Trụ cột nội dung","04","Nghiên cứu • Công nghệ • Chăm sóc • Cộng đồng")
    b.metric("Bộ trò chơi vật lý","132 thẻ","8 nhóm thẻ theo cấu trúc dự án")
    c.metric("Bản đồ hành trình","64 ô","4 vùng trải nghiệm")
    st.subheader("Khám phá CHẠM Hub")
    cols = st.columns(3)
    items = [
        ("📊","Hiểu đúng","Tìm hiểu kiến thức nền tảng và các dấu hiệu cần lưu ý."),
        ("🧭","Ứng xử nhân văn","Thực hành cách giao tiếp và hỗ trợ trong tình huống đời sống."),
        ("🎲","Học qua trải nghiệm","Rút thẻ, giải quyết tình huống và nhận phản hồi.")
    ]
    for col,(icon,title,desc) in zip(cols,items):
        with col:
            st.markdown(f'<div class="panel"><div style="font-size:2rem">{icon}</div><h3>{title}</h3><p class="soft">{desc}</p></div>',unsafe_allow_html=True)
    st.info("Hãy chọn một không gian ở thanh bên để bắt đầu hành trình.")
    st.caption("CHẠM Hub là nền tảng thông tin đồng hành cùng trò chơi giáo dục CHẠM.")

# --------------------------- MODULE 1 ---------------------------
elif page == "📊 Hiểu về Alzheimer":
    hero("MODULE 01 · NHẬN THỨC", "Hiểu đúng để không vô tình làm đau",
         "Những thông tin nền tảng giúp nhận diện sa sút trí tuệ và hiểu vì sao sự đồng hành của cộng đồng quan trọng.")
    st.subheader("Một vấn đề sức khỏe cộng đồng")
    x1,x2,x3 = st.columns(3)
    x1.metric("Người sống chung với sa sút trí tuệ","55+ triệu","Ước tính toàn cầu được WHO công bố")
    x2.metric("Ca mắc mới mỗi năm","Gần 10 triệu","Ước tính toàn cầu của WHO")
    x3.metric("Tỷ trọng Alzheimer","60–70%","Trong các trường hợp sa sút trí tuệ — WHO")
    st.caption("Nguồn: WHO, Dementia. Các số liệu là ước tính toàn cầu, không phải số liệu riêng của Việt Nam.")
    st.markdown("#### Sa sút trí tuệ toàn cầu: quy mô dự báo")
    df = pd.DataFrame({"Mốc":["2020","2030","2050"],"Số người (triệu)":[55,78,139],
                       "Loại":["Ước tính nền","Dự báo","Dự báo"]})
    fig = px.bar(df,x="Mốc",y="Số người (triệu)",text="Số người (triệu)",
                 color="Loại",color_discrete_map={"Ước tính nền":"#18324A","Dự báo":"#55A88B"})
    fig.update_traces(textposition="outside")
    fig.update_layout(height=350,margin=dict(l=10,r=10,t=25,b=10),plot_bgcolor="white",paper_bgcolor="white")
    st.plotly_chart(fig,use_container_width=True)
    st.caption("Dãy số minh họa theo các ước tính thường được trích dẫn từ WHO; khi xuất bản chính thức, nhóm cần đối chiếu năm và phiên bản báo cáo gốc.")
    st.divider()
    l,r = st.columns(2)
    with l:
        panel("Alzheimer là gì?","<p>Alzheimer là một bệnh lý tiến triển của não, có thể ảnh hưởng đến trí nhớ, tư duy, ngôn ngữ và khả năng thực hiện các hoạt động thường ngày.</p><p class='soft'>Không phải mọi trường hợp hay quên đều là Alzheimer. Chẩn đoán cần được thực hiện bởi nhân viên y tế.</p>")
    with r:
        panel("Điều CHẠM muốn thay đổi","<p>Giảm hiểu lầm và định kiến; khuyến khích giao tiếp kiên nhẫn; giúp học sinh và cộng đồng nhận ra vai trò của sự tôn trọng, hỗ trợ và kết nối.</p>")
    st.subheader("Bốn trụ cột của CHẠM")
    pillars = st.columns(4)
    for col,icon,name,desc in zip(pillars,["🔬","💡","🤲","🌱"],["Nghiên cứu","Công nghệ","Chăm sóc","Cộng đồng"],
                                  ["Tìm hiểu và kiểm chứng","Giải pháp hỗ trợ phù hợp","Đồng hành trong đời sống","Kết nối và lan tỏa"]):
        with col:
            st.markdown(f'<div class="step"><div style="font-size:1.8rem">{icon}</div><b>{name}</b><p class="soft">{desc}</p></div>',unsafe_allow_html=True)

# --------------------------- MODULE 2 ---------------------------
elif page == "🧭 Cẩm nang đồng hành":
    hero("MODULE 02 · CẨM NANG", "Một tình huống — nhiều cách lựa chọn",
         "Khám phá những gợi ý giao tiếp và hỗ trợ trong đời sống. Mỗi người có nhu cầu khác nhau; hãy linh hoạt và tôn trọng.")
    selected = st.selectbox("Chọn tình huống muốn tìm hiểu:",[g["name"] for g in GUIDES])
    g = next(item for item in GUIDES if item["name"] == selected)
    st.markdown(f'<div class="panel"><span class="pill">{g["tag"]}</span><h2>{g["name"]}</h2><p>{g["problem"]}</p></div>',unsafe_allow_html=True)
    left,right = st.columns(2)
    with left:
        st.markdown('<div class="panel" style="border-top:5px solid #D98273"><h3>Điều nên tránh</h3>'+g["avoid"]+'</div>',unsafe_allow_html=True)
    with right:
        st.markdown('<div class="panel" style="border-top:5px solid #55A88B"><h3>Có thể thử</h3>'+g["try"]+'</div>',unsafe_allow_html=True)
    st.info(g["note"])
    with st.expander("Vì sao cách tiếp cận này quan trọng?"):
        st.write("Giao tiếp nên hướng đến cảm giác an toàn, sự tôn trọng và khả năng tham gia của người mắc bệnh. Không có một cách ứng xử duy nhất phù hợp với mọi người.")
    st.subheader("Bạn đã nắm được điều gì?")
    feedback = st.radio("Sau khi đọc tình huống, bạn thấy mình có thể áp dụng gợi ý này không?",
                        ["Có thể áp dụng","Cần tìm hiểu thêm","Chưa phù hợp với tình huống mình biết"],horizontal=True,key=f"fb_{selected}")
    if st.button("Lưu phản hồi của tôi"):
        st.session_state.guide_feedback[selected] = feedback
        st.success("Đã lưu phản hồi trong phiên trải nghiệm này.")

# --------------------------- MODULE 3 ---------------------------
elif page == "🎲 Trạm trải nghiệm":
    hero("MODULE 03 · HỌC QUA TRẢI NGHIỆM", "Chạm vào tình huống — chọn cách đồng hành",
         "Trạm trải nghiệm số lấy cảm hứng từ các nhóm thẻ trong bộ trò chơi CHẠM.")
    tab1,tab2 = st.tabs(["🎴 Rút thẻ tình huống","🧩 Thử thách lựa chọn"])
    with tab1:
        groups = ["Tất cả nhóm"] + sorted(set(c["group"] for c in CARD_DECK))
        chosen_group = st.selectbox("Chọn nhóm thẻ",groups)
        if st.button("✨ Rút một thẻ",type="primary"):
            pool = CARD_DECK if chosen_group == "Tất cả nhóm" else [c for c in CARD_DECK if c["group"] == chosen_group]
            st.session_state.drawn_card = random.choice(pool)
        card = st.session_state.drawn_card
        if card:
            st.markdown(f'<div class="panel"><span class="pill">{card["group"]} · {card["code"]}</span><h2>{card["title"]}</h2><p>{card["scenario"]}</p><b>🎯 Nhiệm vụ</b><p>{card["task"]}</p></div>',unsafe_allow_html=True)
            with st.expander("Xem gợi ý phản hồi"):
                st.write(card["why"])
        st.caption("Lưu ý: đây là bộ thẻ mẫu minh họa tương tác trên web, chưa phải toàn bộ 132 thẻ chính thức của bộ trò chơi.")
    with tab2:
        st.markdown("#### Thử thách: chọn cách ứng xử")
        quiz = st.selectbox("Chọn tình huống",CARD_DECK,key="quiz_card",format_func=lambda c:f'{c["code"]} — {c["title"]}')
        st.write(quiz["scenario"])
        answer = st.radio(quiz["task"],quiz["choices"],key=f'ans_{quiz["code"]}')
        if st.button("Kiểm tra lựa chọn",type="primary"):
            idx = quiz["choices"].index(answer)
            if idx == quiz["answer"]:
                st.success("Bạn đã chọn phương án phù hợp trong tình huống này.")
                st.session_state.quiz_score += 1
            else:
                st.warning("Lựa chọn này chưa phải phương án phù hợp nhất. Hãy đọc phần giải thích để cân nhắc.")
            st.info(quiz["why"])
        st.metric("Lượt trả lời đúng được ghi nhận trong phiên",st.session_state.quiz_score)
        if st.button("Đặt lại điểm trải nghiệm"):
            st.session_state.quiz_score = 0
            st.rerun()

# --------------------------- MODULE 4 ---------------------------
elif page == "💌 Không gian sẻ chia":
    hero("MODULE 04 · KẾT NỐI CỘNG ĐỒNG", "Những điều nhỏ bé cũng có thể nâng đỡ",
         "Một góc để viết lại suy nghĩ, ghi nhận điều đã học và gửi lời động viên.")
    left,right = st.columns(2)
    with left:
        st.markdown("### 📖 Nhật ký cá nhân")
        st.caption("Nội dung chỉ được lưu trong phiên trình duyệt/phiên ứng dụng hiện tại ở bản thử nghiệm này.")
        title = st.text_input("Tiêu đề nhật ký",placeholder="Một ngày kiên nhẫn hơn...")
        body = st.text_area("Điều bạn muốn ghi lại",height=130,placeholder="Hôm nay tôi đã hiểu thêm điều gì?")
        if st.button("Lưu nhật ký"):
            if title.strip() and body.strip():
                st.session_state.journal.insert(0,{"title":title.strip(),"body":body.strip(),"time":datetime.now().strftime("%d/%m/%Y %H:%M")})
                st.success("Đã lưu trong phiên hiện tại.")
            else:
                st.warning("Vui lòng nhập tiêu đề và nội dung.")
        for item in st.session_state.journal:
            st.markdown(f'<div class="panel"><b>{item["title"]}</b><p>{item["body"]}</p><span class="soft">{item["time"]}</span></div>',unsafe_allow_html=True)
    with right:
        st.markdown("### 🕊️ Bức tường lời nhắn")
        st.caption("Bản minh họa: lời nhắn chỉ hiển thị trong phiên hiện tại, chưa được chia sẻ giữa các tài khoản.")
        author = st.text_input("Tên hoặc bút danh",placeholder="Có thể để trống")
        message = st.text_area("Lời nhắn",height=130,placeholder="Gửi một lời động viên...")
        consent = st.checkbox("Tôi không đưa thông tin cá nhân nhạy cảm của mình hoặc người khác vào lời nhắn.")
        if st.button("Gửi lời nhắn"):
            if message.strip() and consent:
                st.session_state.wall.insert(0,{"author":author.strip() or "Ẩn danh","message":message.strip(),"time":datetime.now().strftime("%d/%m/%Y %H:%M")})
                st.success("Đã thêm lời nhắn vào bảng xem trước của phiên.")
            else:
                st.warning("Hãy nhập lời nhắn và xác nhận lưu ý quyền riêng tư.")
        for item in st.session_state.wall:
            st.markdown(f'<div class="panel"><b>🌿 {item["author"]}</b><p>{item["message"]}</p><span class="soft">{item["time"]}</span></div>',unsafe_allow_html=True)
    st.warning("Trước khi mở chức năng cộng đồng công khai, cần bổ sung cơ sở dữ liệu dùng chung, kiểm duyệt nội dung, cơ chế báo cáo/xóa bài và chính sách quyền riêng tư. Không nên thu thập dữ liệu sức khỏe hoặc thông tin nhận diện người bệnh.")

# --------------------------- SOURCES ---------------------------
elif page == "📚 Nguồn tham khảo":
    hero("MINH BẠCH THÔNG TIN", "Nội dung có nguồn — niềm tin có cơ sở",
         "Các tài liệu tham khảo được nhóm sử dụng làm nền tảng xây dựng nội dung giáo dục cho CHẠM.")
    for i,(name,url) in enumerate(SOURCES,1):
        st.markdown(f'<div class="panel"><b>[{i}] {name}</b><br><a href="{url}" target="_blank">{url}</a></div>',unsafe_allow_html=True)
    st.caption("Nhóm cần đọc, đối chiếu và ghi ngày truy cập cho từng tài liệu trước khi chốt danh mục trong hồ sơ.")

st.divider()
st.markdown(
    "<div style='text-align:center;color:#718078;padding:.5rem'>"
    "<b>CHẠM</b> · Thấu hiểu để kết nối – Kết nối để sẻ chia<br>"
    "<span style='font-size:.82rem'>Nội dung mang tính giáo dục, không thay thế chẩn đoán hoặc tư vấn y tế.</span></div>",
    unsafe_allow_html=True
)
