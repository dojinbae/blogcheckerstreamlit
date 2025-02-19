import streamlit as st
import requests, re, json, random, datetime
from bs4 import BeautifulSoup
import urllib.parse as par
import urllib.request
from collections import Counter
from konlpy.tag import Okt


# --------------------- 유틸 함수 ---------------------
def clean_text(inputString):
    # 정규표현식 패턴을 raw string으로 작성합니다.
    text_rmv = re.sub(r'[-=+,#/\?:^.@*\"※~ㆍ!』‘|\(\)\[\]$`\'…%&><》\”\“\’·.~_;]', ' ', inputString)
    return text_rmv


# --------------------- 단어 리스트 ---------------------
# word_listf 리스트만 사용 (필요한 단어들만 남겨두세요)
word_listf = [
    '쌍검', '총칼', '참사', '박도', '진검', '독인', '질싸', '염탐', '도청', '사찰', '책동',
    '암표', '섹파', '무단', '영사', '누드', '연초', '궐련', '담배', '구초', '관연', '영초', '마약', '대마', '야바',
    '참사', '경마', '나가요', '폭약', '야사', '영면', '작고', '익사', '피폐', '임명', '졸사', '병폐', '적보', '마땅',
    '참시', '누두', '애널', '에널', '야동', '마다', '병신', '초짜', '음독', '그자', '씹질', '애무', '오랄',
    '체위', '슴가', '폭약', '폭탄', '폰섹', '폰쎅', '호빠', '후장', '섹시', '씨빨', '야덩', '야시', '오럴', '유흥', '잠지',
    '존나', '노모', '도촬', '띠발', '몰래', '몰카', '미친', '벌기', '벌려', '변녀', '빨아', '빨어', '성방',
    '변태', '색스', '동거', '불륜', '애로', '원조', '최근', '장물', '카섹', '폰팅', '섹골', '섹녀', '쌕스', '펨돔', '펨섭',
    '빠굴', '뻐킹', '난교', '색쓰', '섹쓰', '폰쎅', '문섹', '용색', '웬만', '대략', '날이', '실제', '조금',
    '지속', '여럿', '찐', '대부분', '질사', '야설', '빙신', '발기', '귀두', '페팅', '폰색', '섹마', '야겜', '야껨', '야똥',
    '야섹', '음욕', '자쥐', '재랄', '전라', '좀물', '짬지', '찌찌', '체모', '꼬추', '떡걸', '떡촌', '망까', '보짓', '봉알',
    '뵤지', '불알', '색골', '세엑', '육봉', '싸죠', '쌩쑈', '컴섹', '음란', '색폰', '셀걸', '멜섭', '섹할',
    '잡년', '재랄', '저년', '뻘노', '뽀지', '뽈노', '섹쑤', '컴색', '화간', '음경', '음핵', '비엘', '보지', '자지', '성기',
    '야캠', '나체', '음모', '옥문', '고환', '정액', '색마', '망가', '노콘', '콘돔', '음탕', '거유', '창녀', "야한", "야해",
    "할때", "다른", '에로', '시신', '가장', '년', '다양', '부족', '핸플', '세워', '인분', '실천', '블로그마케팅',
    '않', '이반', '텐가', '대딸', '인마', '참수', '정사', '음부', '도추', '성교', '강간', '수간', '간사', "보내죠",
    '뒤져', '자살', '자위', '지발', '가오', '아다', '빠가', '씹', '한거', '살생', '살육', '테러', '난자', '너무',
    '당연', '가질', '여근', '비추', '식인', '옥루', '학살', '음서', '수음', '사의', '상간', '유살', '섹수', '자진',
    '섹수', '요절', '절사', '요함', '국부', '게이', '남색', '파정', '게네', '밤일', '자결', '딜도', '갈보', '살육',
    '척살', '압살', '시역', '역살', '활살', '유살', '불구', '색녀', '대범', '도범', '전범', '혼음', '윤간', '능욕', '야바',
    '아편', '애액', '퀴어', '살인', '창기', '춘부', '포주', '침노', '취한', '야양', '겨웅', '회신',
    '고2', '고1', '고3', '계모', '처자', '과비', '떨', '각하', '계부', '팸', '가결', '가득한', '가어',
    '감정이', '강을', '같네', '것도', '것은', '게으른', '격하', '결여', '곁들인', '관련', '그만큼', '그분', '그에', '꼬물',
    '끊고', '나라는말', '낫다', '내릴', '내블로그', '내에서', '내용은', '네이버에', '높다', '느끼는', '느릿', '다네이버',
    '닫는', '담을', '더위', '돼기', '돼야', '되는것', '되지', '듣고', '들인', '로추', '류요', '많다', '머물', '멍한', '며미',
    '목하', '바로키', '방금', '배워', '병을', '보내세요', '분문', '사는', '사람이', '삶에', '상위노출', '슬픔에', '습득', '시서',
    '시청', '신중', '안에다', '어다', '어떤경우', '어려워', '어르', '에대한', '에들', '에유', '여뉴', '여이', '예민하게', '와함께', '완료',
    '완벽', '욱하는', '울하', '워우', '원래', '위해서', '유난', '의외로', '이것', '이내에', '이상을', '이어짐', '읽었다', '있는지', '재방',
    '재의', '저하', '정신적', '제잘', '줄고', '지닌', '챙겨', '충분히', '친구가', '침에', '커뮤', '판박', '포함'
    # (필요한 단어만 남겨두시고, 목록을 축소할 수 있습니다.)
]


# --------------------- 텍스트 처리 함수 (word_listf만 체크) ---------------------
def process_blog_text(text):
    # 줄바꿈 및 공백 제거 처리
    linea1 = text.replace("\n", "")
    linea2 = str(linea1)
    re.sub('[^A-Za-z0-9가-힣]', '', linea2)
    line1 = clean_text(linea2)
    line2 = line1.replace(" ", "")

    # word_listf 단어 등장 횟수 확인
    penlistf = []
    for word in sorted(word_listf):
        count = line2.count(word)
        if count > 0:
            penlistf.append(f"{word}: {count}")

    total_chars = "총 글자수 : " + str(len(line2))

    # 명사 추출 및 빈도수 계산 (2회 이상만 표시)
    okt = Okt()
    nouns = okt.nouns(line1)
    count_dict = dict(Counter(nouns))
    for key in list(count_dict.keys()):
        if len(key) == 1:
            del count_dict[key]
    sorted_items = sorted(count_dict.items(), key=lambda x: x[1], reverse=True)
    mainlist = [f"{key}: {value}" for key, value in sorted_items if value >= 2]

    return {
        "cleaned_text": line2,
        "total_chars": total_chars,
        "penlistf": penlistf,
        "mainlist": mainlist
    }


# --------------------- URL 처리 함수 ---------------------
def process_blog_url(url):
    # 모바일 버전이 아니면 변환
    if 'm.blog' not in url:
        url = url.replace('blog', 'm.blog')
    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as e:
        st.error(f"URL 요청 실패: {e}")
        return None
    soup = BeautifulSoup(response.text, "html.parser")
    container = soup.select_one("div.se-main-container")
    if container is None:
        st.error("블로그 본문을 찾을 수 없습니다. URL을 확인해 주세요.")
        return None
    text = container.get_text().replace("\n", "")
    return process_blog_text(text)


# --------------------- Streamlit 앱 UI ---------------------
st.title("블로그 텍스트 분석기 (word_listf만 사용)")

input_mode = st.radio("입력 방식 선택", ("블로그 URL", "직접 텍스트 입력"))

if input_mode == "블로그 URL":
    blog_url = st.text_input("블로그 URL을 입력하세요")
    if st.button("분석 시작"):
        if blog_url:
            with st.spinner("블로그 내용 크롤링 중..."):
                result = process_blog_url(blog_url)
            if result:
                st.subheader(result["total_chars"])
                st.write("※ word_listf 단어별 등장 횟수")
                st.write(result["penlistf"])
                st.write("※ 명사 빈도수 (2회 이상)")
                st.write(result["mainlist"])
                with st.expander("클린된 텍스트 보기"):
                    st.text(result["cleaned_text"])
        else:
            st.warning("URL을 입력해 주세요.")
else:
    blog_text = st.text_area("블로그 글 내용을 직접 입력하세요", height=300)
    if st.button("분석 시작", key="text"):
        if blog_text:
            with st.spinner("텍스트 분석 중..."):
                result = process_blog_text(blog_text)
            st.subheader(result["total_chars"])
            st.write("※ word_listf 단어별 등장 횟수")
            st.write(result["penlistf"])
            st.write("※ 명사 빈도수 (2회 이상)")
            st.write(result["mainlist"])
            with st.expander("클린된 텍스트 보기"):
                st.text(result["cleaned_text"])
        else:
            st.warning("분석할 텍스트를 입력해 주세요.")
