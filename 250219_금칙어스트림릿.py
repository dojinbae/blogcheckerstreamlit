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
              '시청', '신중', '안에다', '어다', '어떤경우', '어려워', '어르', '에대한', '에들', '에유', '여뉴', '여이', '예민하게', '와함께',
              '완료', '완벽', '욱하는', '울하', '워우', '원래', '위해서', '유난', '의외로', '이것', '이내에', '이상을', '이어짐', '읽었다',
              '있는지', '재방', '재의', '저하', '정신적', '제잘', '줄고', '지닌', '챙겨', '충분히', '친구가', '침에', '커뮤', '판박', '포함',
              '숙한', '제부', '엄청', '무료', '최고', '최초', '무척', '강추', '추천', '되게', '발기', '콘돔', '야싸', '만냥',
              '콘돔', '부분', '초점', '체팅방', '썰툰', '핑두', '옥링', '표적', '내돈내산', '최저가', '좋아요', '비싸다', '싫어요',
              '효과', '예쁜', '멋진', '기준', '성인용', '성기구', '성생활', '성도구', '성용품', '권장',
              '창피해', '야오이', '학생', '좋습니다', '주세요', '하세요', '갈수', '걸림', '결핍', '됩니다', '겁니다', '습니다',
              '그럼', '기에', '나때', '내는', '넘어', '놓치', '따라', '가능', '들어', '들었', '들을', '같습니다', '드릴게요',
              '천거', '드립니다', '발라', '넣어', '후퇴', '활발', '혹은', '구건', '과전', '특정', '추진', '쳐줘', '게모', '실물',
              '처하', '주중', '나이', '해새', '함이', '한변', '개씩', '각지', '가편', '필요', '펼쳐', '주게',
              '전적', '전문', '저희', '있어', '인근', '이처', '이죠', '무슨', '맞이', '려고', '떠나', '원인', '외롭', '될때',
              '동을', '데에', '다녀', '오랜', '얻어', '어나', '야추', '않게', '심한', '성으', '빠른', '빠르', '분한', '부터',
              '보입', '변화', '때는', '과에', '고쳐', '늦은', '는지', '느슨', '뇌가', '높이', '내용', '장례',
              '다열', '리게', '만히', '방출', '분의', '어릴', '언제', '요인', '음의', '인까', '있지', '자가', '작은', '될수',
              '정확', '주요', '주의', '하기', '한계', '할이', '해내', '근데', '투입', '되다', '써서', '하는데', '하는일', '수있다', '당일',
              '하더라도', '없이', '줘서', '이렇게', '됐다', '없다', '자내', '원으', '가락을', '가슴이', '거라', '결과가',
              '고맘', '과여', '기간', '꿰메', '나갈', '나근', '느라', '는가', '풀려', '하느', '하는법', '호자', '혹이', '편한', '평소',
              '는것', '는다', '때처럼', '떼는', '무난한', '므로', '미세', '반면에', '발생', '변을', '상으', '슴부', '쓰이', '앉아',
              '어일', '에예', '에요', '옆에서', '예를', '옮겨', '옮기다', '응하', '이거', '이거나', '이들', '이럴때', '있을',
              '정기적', '직이', '타날', '걸려', '고페', '그린', '기한', '날씨가', '로리타', '직접', '질', '또는', '및', '골치',
              '남을', '남중', '넓다', '넓어', '넓어서', '다운이', '던데', '된다', '따뜻한', '리를', '반이', '볼게', '분들', '분위기',
              '새벽', '서초', '세게', '수령', '에앞', '옆쪽', '오히려', '와서', '요해', '우선', '위기의', '이는', '재밌게',
              '전체', '좋은', '지점', '쫓기', '차분한', '천천히', '최장', '편안', '한데', '한분', 'zon', '가늘', '가볍게', '감한',
              '같다고', '개인', '것이', '게가', '겠다', '고말', '그렇듯', '근처에', '노예', '조회수', '지털', '친해', '팁이', '파이가', '하면되',
              '나란', '나오면', '나중에', '남겨', '늘려', '니파', '다추', '다행이', '됐고', '되더', '든다', '따뜻하', '똑같이', '리미',
              '마음만', '마지막', '많은것', '먼저', '무던한', '무욕', '박에', '번째', '본래의', '비는', '뽑아', '서아', '살기', '매우',
              '세월이', '시피', '싶다', '안쪽', '않은', '억하', '업사', '없지', '에서의', '연속', '열려', '온이', '올해', '옵니다',
              '완전히', '요개', '요나', '우측', '웃긴', '이번엔', '인가제', '인데요', '잃어', '장이', '정확도', '제3', '져서', '좋겠네',
              '즈스', '집니', '최근에', '최대', '투머', '트스', '편의를', '편하', '피부가', '하면서', '하셔서', '한장', '했네요',
              '했다', '효율', '힘들어', '힙한', '중1', '중2', '중3', '되어', '나트', '증가', '참여', '만성',
              '에소', '섞여', '되고', '쌓인', '기존', '승이', '쪄서', '해여', '러자', '그중', '눌러', '맞춰', '기본', '본적', '름이',
              '이줄', '순히', '낮아', '있던', '올려', '각각', '측면', '어는', '여국', '개의', '트의', '가며', '널이', '비춰',
              '붙어', '있던', '닿는', '좁아', '시야', '또한', '낮고', '쓰여', '이외', '될것', '상시', '표로', '검사장', '세월이',
              '신체의', '습관을', '그렇다', '중에서', '세개의', '동시에', '더불어', '갔다', '갔다온', '개월', '마음을', '며칠', '빨라',
              '이곳', '저의', '좋으', '타일을', '합리적', 'ㄱㄱ', '훌륭한', '꾸준히', '경솔', '귀한', '눈앞에', '달이', '되나',
              '때도', '뜻밖의', '무서', '미래의', '벌어', '생긴', '스럽게', '실상', '않아도', '었다', '은근', '의미', '의지가', '이미',
              '임지', '책임', '초1', '초2', '초3', '초4', '초5', '초6', '추측', '트라', '할만', '할수록', '습관이',
              '가줄', '개설', '검색어', '결국', '그를', '느냐', '다각', '다룬', '댓글', '되겠어', '때에', '를살', '모으', '목적',
              '반대로', '사용자', '솔직히', '시장에', '아래', '여겨', '여기', '여기를', '왼쪽', '유입', '의주', '이웃',
              '저는', '관이', '그러면', '기각', '내거', '누구든', '더많은', '더부룩한', '바뀐', '방해', '불안하게', '스처', '쓸데없는',
              '안돼', '온전한', '전책', '절로', '정으', '천재지변', '큰힘', '한달', '함께극복',
              '가생', '간절', '감정의', '감정이', '같은', '게나', '겠습니다', '견뎌', '고식', '고퇴', '과지', '관계가', '관심이',
              '극의', '긍정적', '기르', '나느', '나라의', '놓고', '놓는', '느려', '는대', '님이', '답답하고', '데가', '도와주는', '도착해',
              '동작을', '되길', '되도록', '된다면', '드시다', '똑바로', '먹고', '무엇을', '무엇인가', '바랍니다', '반드시', '받는데',
              '발의', '변화가', '보인다', '봅니다', '봤어요', '부정적인', '분기', '불쾌', '사회부', '사회적', '살다보면', '생활의', '스유',
              '아칭', '안되', '안됨', '알맞은', '애는', '어려울때', '어려움', '어렵고', '없음', '여간', '여어', '여주고', '와같은',
              '와의', '울때', '으키', '을용', '의불', '의집', '인스트', '일관', '일반인', '있는것', '있음', '잊는', '잦은', '저히', '적갈',
              '적절한', '전후의', '좋아한', '증식', '청함', '체계적인', '최소', '출수', '충분한', '코로나이', '가벼운',
              '할수있는', '함께한', '해봐', '햇볕을', '현저', '화와', '흔한', '흥미를', '힘들다', '힘들게',
              '경험이', '고된', '공부중', '금물', '기징', '담에', '더어', '떼어', '똑같은', '로수', '멀쩡', '무리하게', '무엇이든',
              '서멀', '손아', '심하다', '아니지', '안되는', '안색이', '어렵게', '어렵다', '여러번', '여야', '오늘의', '이흐', '일어난',
              '일인', '자유롭게', '장애우', '적어서', '좋게', '진모', '차코로나', '채워', '첫째', '코로나의', '파이어족', '폼이', '함유',
              '어머', '붙여', 'ㅎㅎ', '레즈', '네시', '빠짐', '해줄', '개해', '이번달', '특별한', '부산에', '드디어',
              '만들게', '타일로', '즐거워', '아주특별', '있는사람', '나잠', '교도', '깜빡', '하듯', '임의', '레르', '시속', '닭을', '응과',
              '들썩', '벌렁', '야단', '짐이', '아의', '화형', '따듯한', '능률적', '귀찮다', '방안을', '은은한', '강남불', '스컴', '려니',
              '실히', '닮은', '태어', '공통', '요언', '제외', '이런이', '간접적', '의생활', '귀가', '말한', '중간',
              '닭과', '기피', '기회', '책이', '되려', '한물', '깨나', '촉진', '출근길', '겨이', '넘쳐', '될까', '의날', '필수', '증극',
              '데주', '맞는', '심지어', '났어요', '걸렸다', '어느덧', '못하게', '림돌이', '말할수', '해가지고', '제공하는',
              '강생', '개다', '굽기', '귀엽다', '길찾', '나와라', '만지는', '먼거리', '멀지', '방예', '별개', '서모양', '선생님과', '술로',
              '시반', '신기방기', '싶어요', '얇은', '업종', '에계', '오른쪽', '요설', '원하는', '이네요', '일후', '죽으', '착한',
              '찾으러', '하얀색', '행복한', '흙만', '흙을', '최적화', 'av', '그새', '히사', '시하', '낳는', '아님', '반기', '차표',
              '진배', '게고', '고맙', '나홀', '미뤄', '났지', '잊지', '멤버', '종의', '기여', '자출', '찜찜', '잔뜩', '월북', '회도', '남들',
              '가뭔', '나기', '종합', '해는', '인신', '판업', '업신', '승인', '다꾸', '뭔지', '만생', '고프', '과물', '낫지', '실건', '향후',
              '크나', '딱히', '낸다', '불허', '다잠', '관관', '려면', '사드', '간새', 'THE', '좋았던', '한일중', '강렬한', '홀린듯', '교보문',
              '보문고', '이나여', '끝없는', '배우님', '같아서', '일종의', '왜이리', '맛있는', '은누가', '화나는', '겉으로', '세상에', '듯하다',
              '자신과', '보았다', '한단계', '제일좋', '결과물', '뒤늦게', '지식이', '라든지', '일수도', '최선을', '간단하게', '재미있게',
              '네이버스', '알수없는', '나의가치', '기도하다', '아름다운', '가볼만한', '가워', '가지를', '가펼', '간곳', '갖기', '개가', '걸까', '걸보',
              '것만', '게동', '게속', '결혼발표', '경찰서', '경체', '고교', '고기를', '고더', '곳곳에', '공파', '굉장히', '교체', '굳게', '굴로',
              '귀여운', '규해', '그녀를', '그들은', '금세', '기러', '김히', '까봐', '꽤나', '꿈이', '끝은', '나간', '나달라', '날씨에', '날차',
              '남자의', '났는데', '내다', '내보', '너가', '너의', '농락', '놓아', '니너', '니동', '다려', '닫아', '대다', '대한다',
              '더는', '더욱더', '덕에', '데대', '도겨', '독한', '동생이', '됐으니', '되었는데', '되었으면', '들뜬', '라무', '럽스타', '리곤', '마는',
              '만기', '만새', '많아서', '말린', '말미', '맛이', '맞고', '맡기', '맨날', '멋대로', '몇분', '목소리의', '못해요', '무섭', '물려',
              '바다의', '밖에서', '밟는', '번다', '볼까요', '붉은', '비치로', '산산', '서거', '서너', '서완', '서추', '선뜻', '설분', '세먼지',
              '순간을', '시원한', '신비한', '실검', '실려', '실새', '실컷', '싶지만', '아무런', '아쉽게도', '아큰', '악랄', '악물', '안눈', '안하고',
              '알게된', '암리', '앞에서', '애들', '야기', '양처', '어마', '어색한', '어집', '업기', '에곳', '에답', '에우', '에커', '였지만',
              '영기', '영하의', '요저', '우리의', '우차', '운하', '울을', '웃도', '원의중', '육관', '의빙', '이금', '이런게', '이빠',
              '이전의', '인파', '입안', '자극적', '자나와', '자로', '자리에', '자연이', '잘알', '장그', '장은', '저무', '적극적', '전재',
              '정달', '준영', '중여', '즐겁게', '지금은', '지나가는', '지망', '지여', '지역', '지컬', '직정', '진이자', '쫓는', '차주', '창밖', '최상',
              'ㅋㅋ', '캐스', '커녕', '터라', '파도가', '플캐', '하나가', '한번다', '해귀', '행지', '호쾌한', '희롱', '히보고', 'ㅠㅠ',
              '가격대', '감옥에', '건설적', '것입니다', '게끔', '게다가', '계시나요', '참석', '태도를', '해도되', '험한', '지금처럼',
              '고플', '공을', '괴롭히는', '극히', '기록한', '기연', '꾸리기', '나눈', '다러', '다뤄', '다시시', '도는', '때리는', '럽스타',
              '로준', '린아들', '못하다', '바일', '받았다', '벗고', '비참한', '사용할', '살고있다', '새해에도', '속이다', '수용소', '시험은',
              '실패는', '쓰게', '앞으로도', '억울함', '여보', '여사', '연두색', '와전', '우리은', '우여곡절', '위쪽', '유명인', '의자녀',
              '이발병', '이야기를', '이책은', '일반적', '입니다만', '있다가', '자기자신', '잔사', '잠기', '주사용', '중노', '지극히', '갑니다',
              '같지', '개만', '개별', '개제', '개한', '거대', '것들이', '게조', '고무적', '곳다', '그때의', '그전', '그전에', '급이', '기내',
              '끝날', '나에게는', '노란색', '노력을', '녹색', '놓친', '다시중', '다워', '다행히', '덮인', '데고', '되자', '든사람',
              '따끈한', '또하나의', '락시', '랑사', '린자', '마법의', '만간', '모호한', '모호함', '목숨을', '무래', '묻히는', '미래집',
              '밭은', '백만', '별도로', '본의', '부어', '부어라', '사업을', '생길', '서갑', '서중', '성글', '속보', '수많은',
              '쉬운', '스디', '스찬', '시새', '시정', '쓰니', '아쉬운', '알았는데', '앗아', '얘기', '어떤지', '어른이', '얼이',
              '영으', '예감은', '와국', '으라', '을영', '의로', '의술', '의회', '이다가', '이번주', '이번주도', '이어져', '이지금', '이초',
              '인공의', '인회', '일게', '일본의', '자유로', '전후로', '점정', '조만간', '종특', '주누', '지라도', '지사장', '짚어', '짧았다',
              '찾아서', '첫달', '추후', '치고는', '치워', '쿠퍼의', '탈당', '트기', '티플', '풍부한', '필히', '후과', '히동',
              '갔네', '갔어', '개런', '개체수', '건바', '권은', '깔끔하게', '끊어진', '끝나', '남아있는', '남에', '노릇', '놀고',
              '단할', '당한자', '대체', '데는', '된지', '될놈될', '드셔', '든든하게', '떠서', '록색', '맛있게', '몇십', '문밖', '묻어', '물씬',
              '민은', '반출', '방중', '보충', '부워', '빠는', '사랑받는', '세히', '소하고', '수중에', '숨은', '시구', '시네요', '식메', '식중',
              '실게', '십만', '썰어', '씻어', '아응', '아하니', '얘기', '에상', '여고', '여파', '연실', '영끌', '예전에는', '올리시',
              '요입', '음식에', '의로', '의에', '이녀석', '이좋', '익혀', '자세하게', '작소', '재는', '적힌', '전혀', '절상', '절은', '제대',
              '제대로된', '주건', '준비도', '지배', '진하게', '짜스', '짭조름', '쫙쫙', '쯤에', '최저', '치여', '카키', '커키', '켜켜이',
              '크다', '편에', '한상이', '합쳐', '후락', '휴일', '흰색', '가까스로', '가독성', '가뮤', '각조', '간다고', '간색', '갈려', '감설',
              '갖는', '거져', '검으', '게부', '겨주', '경찰조', '고찬', '관심없는', '구회', '군수', '궁금하다', '그시', '그야', '그후로', '극강의',
              '기더', '길로', '깔끔하고', '꺼내', '껴안고', '나들', '나려', '남다', '남았다', '낭만적', '내전', '냈다', '네가', '느무', '님장',
              '다보여', '다사고', '다음번', '담백한', '당신과', '데려', '데온', '도찰', '독보적', '독을', '들일', '딱이', '떴다', '띵작', '랄까',
              '러진', '만엔', '멸망', '모든걸', '모배', '몰아', '묵직', '뭐든', '반겨', '반관', '번호로', '벗겨', '보이실', '보적', '보통은',
              '본진', '부결', '부근', '불과', '불호', '빨간색', '빨이', '사비', '사형', '서울에서', '설희', '속한', '순국', '쉽네', '스영',
              '스쳐', '시판', '신규', '씬이', '아쉽다', '안보', '알을', '압도적', '애틋한', '야생', '얽혀', '연배', '오토시', '와한', '운터',
              '원할', '음속', '음이찡', '의군', '의온도', '이번에는', '이임', '이흰', '익이', '입국', '있자', '자든', '작전중', '장소를', '저곳',
              '저류', '저아', '종전', '주십', '준비된', '줍줍', '중앙선', '지구는', '지식iN', '진그', '진새', '쫄깃', '쫓다', '참고해', '채고',
              '초간단', '출신', '친그', '캄캄한', '태양이', '트수', '트정', '특별히', '파란색', '파악', '팔당대교', '퍼센', '편선', '하다보면',
              '하시길', '하파', '현장에서', '호의', '화스', '회차로', '후가', '훼손', '히가', '히네', '히들', '가급적', '거려', '경정', '고급진',
              '급진', '급하게', '급한성격', '기름진', '기필코', '깔끔히', '나집', '노맛', '녹아', '니상', '다계', '다대중', '다석', '닫이', '달달한',
              '대비해', '데인', '동안에', '됐어', '득기', '때쯤', '띄게', '무리한', '물의', '물컹', '바람이', '반심', '베어있는', '볶이', '분명히',
              '사용도', '살살', '상큼한', '색적', '소문이', '수다를', '심각', '아닙니다', '알아봐', '야이', '여유로운', '역국', '연말정', '옥우',
              '온을', '운에', '이갓', '이뤄진', '이살', '이열리', '이틀전', '임하다', '입싸', '전반적인', '정갈하게', '정밀한', '제명', '직관적',
              '진득', '집중적', '집피', '짓기', '짭쪼름', '차가운', '체력이', '칭하다', '트오', '튼튼한', '폭신', '풍겨', '하셨다', '향은', '호에',
              '홍대에', '흐트러', '가가가', '가짜뉴스', '갑론을박', '객관적', '거시', '검은색', '경호처', '공관', '공권력', '관저', '구라', '국방',
              '국정', '김종', '김처장', '꼰대', '낙태', '날기', '놓지', '대선', '대통령실', '대통령직', '던져', '동성애', '뒷배', '때구', '룸카페',
              '모씨', '무속논란', '방탕', '범죄자', '보수정권', '빠지고', '뿐이', '사상', '상용화', '서민주', '성관계', '성매', '성범죄자', '성욕',
              '성행위', '섹스', '손바닥에', '수위', '싫다', '야당', '억원', '없애고', '역이', '올바르', '유지해', '육군참모', '육하',
              '은존', '이쟁', '인지모', '인하고', '장으', '재인', '재해', '적고', '절손', '정의당', '정책', '져주', '허용되는', '후보',
              '조용히', '지나침', '지난해', '천공의혹', '청와대', '출산문제', '통화기록', '튜브방', '틀어', '해말', '행동이', '변사체', '노브라',
              '엉밑살', '가볍다', '값이', '건양다', '건조비', '관용', '광범위', '구형', '군은', '권다', '그때가', '그차', '기감', '깡충', '꽉꽉',
              '끓여', '내스', '당선', '데캡', '드베', '등등등', '때문이다', '라변', '로화', '린아이', '메워', '무엇보다', '문앞에',
              '민첩', '밑줄', '박하다', '발이', '보실', '비친', '삶아', '세계에서', '속상', '수이', '스주', '시풍', '싫어해', '아무튼', '안속',
              '얇아', '얕게', '어떠한지', '어색하다', '얻은것', '에매', '연령대', '올한해', '용이하다', '월보', '으흐', '이어주', '인상적인',
              '있듯이', '자중', '적가', '전통적인', '즐거웠다', '지금까지', '처음보다', '최적의', '친숙', '커피수혈', '트코', '편리하다',
              '풍성한', '형의', '게세', '금네이버', '네이버카', '대하여', '로그인후', '리널', '바보야', '부과', '세자', '인변', '정당',
              '정보유출', '제공받아', '준비중', '확인할수', '환급계좌', '가탈', '탈세', '끔찍', '단위', '라여', '당국', '밀려', '바르게',
              '동해야', '감당할', '예인이', '과하다', 'od', 'SM엔터', 'YG엔터', '감청', '걸맞은', '검토중', '경북고',
              '고대중', '고려대출', '공급가', '공동', '관공서', '관청', '관행', '광역시', '괴담', '구체적', '국세청이', '굵직', '꼼꼼히',
              '끄읕', '납부내역', '논란이', '당금', '대단하다', '리위', '명백하다', '모친', '무사유', '무사회', '미스에', '바쁘다', '반공',
              '발위', '분당불', '불미', '불일치', '불후', '브더', '비집', '사용금액', '사임', '사평대로', '상기', '수억', '스개', '스삼',
              '안애', '앙대', '애에', '야심차게', '에프엑', '연대의', '예다', '요는', '요증', '유출된', '익숙해', '인기몰이',
              '인박', '인선', '일베', '일체', '재개', '적수', '전소', '주상', '즉시', '지잡', '초품아', '층수', '키가', '택대', '트워',
              '편리한', '프로듀', '하랴', '합조', '획기적인', 'ㅡㅡ', '결방', '계다', '고이상', '네이버영', '늙고',
              '니수', '다국', '대해서는', '대화중', '독다니엘', '류여', '린가', '말귀를', '못알', '밍아웃', '법위반', '부투',
              '속세와', '순간에', '심오한', '싸우는', '아줌마가', '여채', '오락가락', '은평을', '이용하여', '제출한',
              '짜고', '키가', '하고나서', '한것같다', '함께하는', '화군', '확정', '가기로', '내근처', '노느', '니마', '니인', '두르고', '뭐해',
              '밝아서', '버스타고', '비검', '석자', '순식간', '어딜', '어울리는', '요메', '워매', '위층', '은라', '이쁜거', '인반',
              '조화로운', '직후', '진마', '커피도', '킬라', '홀짝', '흑흑', '거국', '공적인', '구금', '국민들이', '그보다', '나라가', '대규', '대비한',
              '대안', '되기전에', '무늬만', '버팀', '서도고', '신뢰성', '이B', '잠재적인', '저렴한', '적정성', '중단', '중으로', '징역형', '최악의',
              '페에', '공가', 'ero', 'IMF', '개국', '개수', '건거', '게돈', '게차', '겨냥',
              '고객님', '공정위', '권보', '귀하의', '금리동결', '금리역전', '금리인상', '젖꼭지', '자기위로',
              '금융위기', '까닭은', '껑충', '끈적', '날아간다', '남성고', '넓히고', '노동절', '딸딸이',
              '노하우를', '누구나쉽', '느님', '대표는', '대플', '데통', '도레', '돈되는', '동사무소',
              '듭니다', '뢰하', '매니', '몇백', '못사', '못산다', '뭉칫돈', '바꿀때', '반도체법',
              '받아요', '뱅크런', '벼랑', '분쟁', '사랑을', '사회가', '샀다', '서변호사',
              '성큼', '세밀한', '소상', '수입물가', '수히', '슨지', '시간대', '식보', '신흥강자',
              '아라중', '아시나', '안정성', '약하', '어카', '언니는', '여매', '여중', '연기금',
              '연준금리', '열풍', '우리파', '원전', '원전수출', '원활한', '음쓰', '일괄', '일매',
              '일선에서', '저공', '적개', '전남편', '전부인', '점유율', '제일싸', '제일중', '조명하',
              '종결', '주택공사', '죽자', '중국한국', '중심의', '즈로', '증진', '천만명', '최첨단',
              '추가적인', '침체', '퀘어', '탈이', '터무니', '통상적', '틱톡금지', '파란만장', '평수',
              '폭풍성장', '푼다', '피의', '한국호주', '함게', '해지다', '형화', '확산', '회사와',
              '젖꼭지', '자기위로', 'ty', '고등학교', '국보', '근방', '급장', '기까지', '끝으로',
              '나누기', '나의원', '난감', '네이버가', '단나', '뚜렷', '련한자', '류시', '미비', '보건소',
              '상편', '생님', '셔야', '수백명', '시도', '쌓고', '약은', '의체', '의하면', '잠복',
              '저렴하다', '제일많이', '지참', '직할', '초등학교', '치한', '한국보건', '덥지', '써매',
              '업비', '개서', '힘드네', '상대적', '문의는', '쓰다보니', '뇌피셜',
              '코로나시', '운영하는', '골이', '중히', '복무중', '군병원',
              '일교차', '동기들', '귀중한', '강하게', '곧은', '눌려', '은디', '한번씩',
              '구사항', '접근할', '네이버방', '딸딸이', '후연', '짧아진', '짐은', '슴연', '면역의',
              '끝전', '끝난', '너도', '에교', '이름도', '이제곧', '열정적',
              '해결책을', '병만', '근본', '깊이있는', '시느', '이글이', '누구나한', '전달하다',
              '던저', '겨지', '니익', '겉에', '곧게', '덮여', '도외', '적장', '나내',
              '더만', '휘어짐', '요소로', '촉촉한', '구조적', '수직으로', '라교', '어딜', '고개를',
              '아름다움', '만만치', '받았어', '섬세한', '나흔', '이몸', '적특', '맡길', '전에',
              '성피', '절근', '친입', '조심해', '제일큰', '균형을', '상정', '게난', '꺽인',
              '단순이', '돌발', '물렁', '소으', 'A급', '도머', '흔이', '격상', '휘어진', '제목을',
              '과학고', '괴리', '그래야만', '그매', '노려', '두배', '라한자', '매장수', '비부동산',
              '상메', '성현', '식디', '쌉쌀', '암물', '업스', '에둘러', '연발', '예산을', '위치콘',
              '읊기', '자신만의', '장속', '장직', '저병', '컬래', '탓에', '품위', '혀를', '형유',
              '가려지다', '가수분', '각광', '간후', '감기가', '검사부', '급병', '급차', '께서도', '끝낸',
              '나보다', '도박', '드물게', '딘이', '무월', '물게', '반감', '뱃속', '변요', '상병',
              '시큰', '아등', '아픔이', '오틱', '왕은', '진보', '천대', '침대가',
              '유연하게', '유타기', '이마저', '이마저도', '이튿날', '인천비', '일째', '적진', '즈음',
              '탈락', '태아탈장', '풍발', '한꺼번에', '함량', '행여', '후풍', '힘듭니다',
              '전률', '회복할', '지나서', '읽어주세요', '일부로', '이딸', '응해', '신경의', '식혀',
              '상한자', '병원네이버', '맡고', '래끼', '나타났다', '꼈다', '긴이', '기도많이', '과열',
              '결정적인', '각세', 'B차' '혈과', '자척', '차바', '절대적인', '싸여', '군대에서',
              '사격훈련', '뿐만아니라', '뚱한', '동안고', '더욱이', '더더구나', '눈에띄는', '군복무',
              '수류탄', 'ㄷㄷ', '뒤면', '수님', '열정적', '왠만해서', '요쥬', '움직여', '할께', '것',
              '월일', '장함', '요미', '구라', '오오', '민폐', '거임', '저날', '저일', '막실', '뽀짝',
              '샀어', '네앱', 'ㅃㅇ', '갤러', '페에', '훑어', '형식이', '피드백을', '치서', '참다',
              '진작에', '준대로', '여러모로', '어떤식으로', '앞날을', '블로그홍보', '블로그상위', '번져',
              '백까', '데서', '대중적으로', '네이버아이', '네이버시', '네이버블로', '네이버는', '날일',
              '꿰뚫고', '개편', 'I의', '갑지', '과하마', '깜찍한', '단단한', '게야', '고ㅈ', '군더더기',
              '만갤', '만화소', '맡긴', '매력적인', '멘붕', '면갤', '물가상승', '붕이',
              '블랙블루', '뿐입니다', '상승률', '성갤', '스간', '스갤', '스다', '슬하',
              '실업률', 'ㅇㅇ', '압승', '약간의', '여약', '연준', '영연', '오래지', '올때', '월등히',
              '유행하는', '이폰SE', '이폰X', '제롬파월', '줬다', '지식의', '진짜', '차건',
              '차이점', '참아', '채수', '크노', '탄한', '터리', '판매량', 'ㅎㅇ', '한게임플',
              '한손에', '한양이', '휴예', '히갤', '국매', '기뻐', '깜찍한', '단단한', '만갤', '매력적인',
              '블랙블루', '뿐입니다', '약자', '외워', '중학교', '진지글', '같음', '개랑', '겁나', '것다',
              '규어', '그러한', '기사용', '껐다', '끄고', '다ㅅ', '뜻깊은', '락실', '랑구', '린샷',
              '막폰', '맹유', '멜피', '뭐시', '뭐시기', '바로다운', '바로아이', '번쩍', '부드럽다',
              'ㅅㅂ', '사온', 'ㅇㅈ', '얘는', '얘도', '어홍', '온거', '요항', '일환으로', 'ㅈㄴ',
              'ㅈㄹ', '전따', '전익', '전잘', '쨍한', '찍음', '편리하게', '포카', '한파란', '헌이',
              '현타', '황색', 'KTLG', '성낭', '가ㅈ', '재제', '소추', '더버', '기레', '계위', '계업',
              '간데', '다사이', '냅다', '길가다가', '그제', '게잊', '거갤', '가다가', ';;', '자릿수',
              '일코', '일임', '외신', '오뚜', '여초', '실적발표', '스2', '속포', '북을', '미중갈등',
              '미중', '미국한국', '미국은', '물가인상', '매크로', '라동', '국한', '퇴근후에', '주민센터',
              '업무시', '어서울', '실의', '부순', '발역', '모병', '동중', '내부순환', '관동중', '하시어',
              '폭은', '월이전', '여1', '약후', '스내', '서울의', '산중', '동산중', '도금대출', '급행',
              "힣"
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
