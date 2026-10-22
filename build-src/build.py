# -*- coding: utf-8 -*-
"""優健堂 UHealthFit × WiseQuest 靜態網站產生器 · NTD Digital 2026-10-19
位置：repo/build-src/build.py　執行：python3 build-src/build.py　→ 直接輸出到 repo 根目錄（GitHub Pages 的發布根）
改文案的地方：本檔的 SERIES / PRODUCTS / QUIZ / FAQS 資料區、posts/ 內的 12 篇文章、src/style.css、src/main.js
"""
import json, os, re, shutil, hashlib, html as H
from urllib.parse import quote

ROOT = os.path.dirname(os.path.abspath(__file__))
# 依內容產生版本號，加在 CSS／JS 網址後面：內容一改，瀏覽器就會重新下載，不會拿到舊快取
def _ver(path):
    return hashlib.md5(open(os.path.join(ROOT,'src',path),'rb').read()).hexdigest()[:8]
CSS_VER = _ver('style.css'); JS_VER = _ver('main.js')
DIST = os.path.dirname(ROOT)  # repo 根目錄
SHOP = 'https://zh.uhealthfit.com/zh-hant-us'  # 強制美國市場（USD）；根路徑預設為 EUR 市場
SITE_URL = 'https://toniachu2026.github.io/uhealthfit-zh'  # GitHub Pages 網址；綁自訂網域後改這一行重建
IMG = 'https://uhealthfit.com'
LOGO = f'{IMG}/uhealthfit/uhealthfit_zh_logo.svg'  # 導覽列：優健堂（同 uhealthfit.com/zh-TW）
LOGO_WHITE = 'img/uhealthfit-logo-white.svg'  # 頁尾：UHealthFit 白色字標（同 zh.uhealthfit.com 商店頁首）
SHOP_CDN = 'https://zh.uhealthfit.com/cdn/shop'  # 官方商店（Shopify）素材：六大系列情境照、產品實拍
def shop_img(path, width=800):
    return f'{SHOP_CDN}/{path}&width={width}'
KLAVIYO_COMPANY = 'Xxa5rp'
KLAVIYO_LIST = 'TKC3Bu'
TODAY = '2026-10-19'

def shop_url(handle):
    return f'{SHOP}/products/{quote(handle, safe="-")}'

# ───────────────────────────── 資料 ─────────────────────────────
SERIES = {
 'eye': dict(name='護眼系列', short='護眼', en='Eye Care', color='var(--c-eye)', organ='肝開竅於目',
   tag='外、內、日夜一次到位', h1='睡覺時，讓眼睛好好休息',
   lead='長時間盯螢幕的一天結束後，眼睛也需要自己的「下班時間」。眼貼負責睡前的外部舒緩、膠囊從內支持、眼霜負責白天——三件合稱「護眼三寶」。',
   situations=['每天盯螢幕超過 8 小時，到了下午眼睛就覺得乾澀、沒電','睡前還在滑手機，早上起來眼睛沒有休息到的感覺','葉黃素吃了一陣子，但長時間用眼後的疲勞感還在'],
   reframe=[('即時舒緩','眼藥水、熱敷眼罩負責「這一刻舒服一點」，它們很重要，但用完就結束。'),('夜間休息','睡著的六到八個小時，是眼睛最長的一段休息時間——冷敷眼貼在這段時間陪著它。'),('內在支持','中醫傳統認為「肝開竅於目」，七味東方養目草本從內支持眼睛的長期健康。')],
   products=['eye-patches','lumiview','eye-cream'], bundle='eye-care-trio',
   combo=('護眼三寶怎麼搭','睡前貼眼貼（外），每天兩次 LumiView（內），白天不方便貼眼貼時擦眼霜（日）。三個產品不是三個選擇，而是一天二十四小時的三個時段。'),
   faq=[('眼貼和蒸氣眼罩有什麼不同？','蒸氣眼罩是熱敷放鬆，十五分鐘結束；冷敷眼貼貼在眼周肌膚上，草本透過肌膚緩緩釋放，陪你度過整晚。兩者用途不同，可以依習慣選擇。'),('我已經在吃葉黃素，還需要嗎？','葉黃素補充的是視網膜相關的營養；長時間用眼後的乾澀疲勞感是另一個面向。兩者不衝突，是否同時使用建議先與醫師或藥師討論。'),('眼貼會進到眼睛裡嗎？','不會。眼貼貼在內眼角、外眼角與下眼瞼下方的肌膚上，不入眼；日本製造、不含防腐劑，過敏回報極少（依品牌內部客服紀錄）。首次使用前先做局部皮膚測試，孕婦請勿使用。')],
   photo=shop_img('collections/1_46cb0e74-a579-49cb-92db-27a44cc036be.jpg?v=1776886629',900), image=f'{IMG}/_optimized/concerns/eye-care-1200.avif', image_fallback=f'{IMG}/products/eye-patches/eye-patches-box-front.png'),
 'dental': dict(name='口腔健康系列', short='固齒', en='Dental Care', color='var(--c-dental)', organ='腎主骨，齒為骨之餘',
   tag='刷牙之外的日常', h1='健康牙齦，穩固牙齒',
   lead='刷牙與牙線照顧的是看得見的表面。每天一次草本膠囊，從內在為牙齦與牙齒的日常健康多加一層支持——也是很多子女替爸媽準備的一份心意。',
   situations=['刷牙很認真，但還是想為牙齦的長期健康多做一點','爸媽年紀漸長，想替他們準備一份每天做得到的口腔保養','在「只有刷牙」與「大工程」之間，想找一個日常的中間選項'],
   reframe=[('表面清潔','牙膏、牙線、漱口水與洗牙負責看得見的表面，是每天不能少的基本功。'),('內在支持','中醫傳統認為「腎主骨，齒為骨之餘」——牙齒的穩固與整體的滋養有關，十味草本從這個角度出發。'),('長期管理','口腔健康是一輩子的事。每天隨餐一次、搭配定期牙科檢查，把保養變成習慣。')],
   products=['dentaforte'], bundle=None,
   combo=('怎麼開始','DentaForte 每天隨餐服用，不需要改變原有刷牙習慣；請持續定期牙科檢查，有任何口腔不適請先就醫。'),
   faq=[('這能取代看牙醫嗎？','不能。DentaForte 是膳食補充劑，不是藥品，也不能取代牙醫的檢查與處置。它的位置是「刷牙之外、看牙之間」的日常保養。'),('要吃多久？','建議至少給自己 4–8 週，作為長期口腔健康管理的一部分；效果因人而異。'),('替長輩購買要注意什麼？','長輩若正在服藥或有慢性健康狀況，請先與醫師或藥師確認。全植物膠囊、隨餐服用，放在早餐旁最容易記得。')],
   photo=shop_img('collections/2_d6d295f9-6329-4973-aad6-05f2a9b122ca.jpg?v=1776886620',900), image=f'{IMG}/products/dentaforte/dentaforte-product-shot-wide.png', image_fallback=f'{IMG}/products/dentaforte/dentaforte-bottle-front.png'),
 'sleep': dict(name='睡眠系列', short='睡眠', en='Sleep Care', color='var(--c-sleep)', organ='心主神明',
   tag='不含褪黑素・配方溫和、不設計為長期依賴', h1='白天放鬆，夜裡好眠',
   lead='壓力大的日子，腦子到了晚上還停不下來。這個系列的原則很簡單：先安撫白天的壓力，支持身體原本的睡眠節律——不靠外力「關機」，狀態穩定後可以停用。',
   situations=['躺下了，腦子還在跑今天的待辦事項','想找不含褪黑素的選項，怕隔天昏沉','工作壓力大，希望夜晚能真正放鬆下來'],
   reframe=[('白天的壓力','中醫傳統認為「心主神明」——夜裡難以放鬆，常常是因為白天沒有「下線」。'),('草本安神','炒酸棗仁、合歡皮、茯神等七味草本，傳統上用於幫助安神放鬆，不含褪黑素。'),('不依賴','中午飯後與睡前各一次，先幫忙放下緊繃；節律穩定後可以停用，之後依需要再開始。')],
   products=['calmoon'], bundle=None,
   combo=('怎麼開始','Calmoon 建議中午飯後與晚飯後／睡前一小時各 3 粒。搭配睡前一小時放下手機、固定起床時間，效果更容易累積。'),
   faq=[('為什麼中午也要吃？','因為這個配方照顧的是「白天的壓力」。中午那一次幫忙放下上午的緊繃，晚上那一次支持自然入睡。'),('會不會隔天昏沉？','Calmoon 不含褪黑素，配方溫和。每個人的感受不同，建議先從建議用量開始觀察。'),('可以和其他助眠產品一起用嗎？','若正在使用任何助眠產品或藥物，請先與醫師或藥師討論，不要自行疊加。')],
   photo=shop_img('collections/Bedtime-Habits-scaled.jpg?v=1785620068',900), image=f'{IMG}/products/calmoon/calmoon-product-shot-wide.png', image_fallback=f'{IMG}/products/calmoon/calmoon-bottle-front.png'),
 'digestive': dict(name='消化系列', short='消化', en='Digestive Care', color='var(--c-digestive)', organ='脾主運化',
   tag='不含番瀉葉', h1='順暢自然，不靠刺激',
   lead='不是不通，是通了還是脹——潤腸與行氣是兩件事。以火麻仁為核心的六味草本，溫和支持腸道的自然節律，不含番瀉葉，節律穩定後可以停用。',
   situations=['久坐一整天、外食應酬後，肚子常常頂著一股氣','想找溫和的選項，不想越吃越多','希望腸道回到自己的節奏，而不是被「催」'],
   reframe=[('潤','火麻仁、生地黃、當歸——傳統上用於潤養，讓腸道不乾澀。'),('行氣','萊菔子、厚朴——傳統上用於行氣消脹，中醫說「脾主運化」，通也要不脹。'),('養節律','每天兩次隨餐，不含番瀉葉；節律穩定後可鞏固一段時間再停用。')],
   products=['herbalflow'], bundle=None,
   combo=('怎麼開始','HerbalFlow 每天 2 次、每次 3 粒隨餐。搭配每天固定時間如廁、多喝溫水、飯後散步十分鐘，更容易養成節律。'),
   faq=[('和益生菌衝突嗎？','益生菌照顧的是菌相，HerbalFlow 的思路是潤腸與行氣，兩者角度不同。是否同時使用請先與醫師或藥師討論。'),('會不會越吃越多？','HerbalFlow 不含番瀉葉等刺激性成分，設計原則是支持節律而非刺激；節律穩定後可以停用。'),('什麼情況該去看醫師？','若有持續性的腹痛、體重明顯變化、排便型態突然改變或出血，請直接就醫，不要只依賴保健品。')],
   photo=shop_img('collections/Inside-1bloating.jpg?v=1785620047',900), image=f'{IMG}/products/herbalflow/herbalflow-product-shot-wide.png', image_fallback=f'{IMG}/products/herbalflow/herbalflow-bottle-front.png'),
 'skin': dict(name='肌膚系列', short='肌膚', en='Skin Care', color='var(--c-skin)', organ='肺主皮毛',
   tag='無類固醇・溫和到可以天天用', h1='鎮靜、舒適，更柔軟的肌膚',
   lead='乾燥脫皮、換季敏感、曬後、蚊蟲叮咬後，或是容易長痘的膚況——東方草本加上透明質酸、維生素 E 與維生素 C 衍生物，為肌膚做好每天的保濕、舒緩與屏障保養。全家可用，美國製造。',
   situations=['換季時肌膚容易敏感、乾燥脫皮','想找一罐全家都能用的無類固醇舒緩霜','油脂與屏障想一起照顧，不只是壓油'],
   reframe=[('屏障','肌膚反覆不穩定，往往是屏障沒有照顧好。保濕與屏障保養要一起做。'),('草本舒緩','蒲公英、紫草、積雪草等草本，傳統上用於舒緩；無類固醇，溫和到可以天天用。'),('日常習慣','早晚各一次，首次先局部測試；搭配清淡飲食與規律作息，膚況更容易安定。')],
   products=['soothing-cream','clarifying-cream'], bundle=None,
   combo=('怎麼選','乾燥、換季敏感、曬後、蚊蟲叮咬後 → 草本舒緩修護霜；易出油、容易長痘的膚況 → 草本淨顏霜。兩者都是外用保養品，可以依部位分開使用。'),
   faq=[('無類固醇是什麼意思？','配方中不含類固醇成分。這是一款日常保養品，不是藥品；若醫師已為你開立外用藥，請依醫囑使用，不要自行替換。'),('小孩可以用嗎？','草本舒緩修護霜設計為全家可用。嬰幼兒或有特殊膚況者，使用前請先諮詢醫師，並先在小範圍測試。'),('淨顏霜會不會太乾？','淨顏霜的思路是「調理油脂＋支持屏障」，含維生素 C 衍生物；若覺得乾，可以只用於易出油部位，其他部位搭配舒緩修護霜。')],
   photo=shop_img('collections/3_e69c85a3-7756-4f7b-8d78-f189c2138e6d.jpg?v=1776886599',900), image=f'{IMG}/products/herbal-soothing-repair-cream/soothing-repair-cream-product-shot-wide.png', image_fallback=f'{IMG}/products/herbal-soothing-repair-cream/herbal-soothing-repair-cream-jar-front.png'),
 'vitality': dict(name='煥顏・活力系列', short='煥顏活力', en='Radiance & Vitality', color='var(--c-vitality)', organ='腎主藏精',
   tag='不要看起來很累', h1='不要看起來很累',
   lead='你要的不是變年輕，是不要看起來很累。外在，用東方草本 × 胜肽的精華幫助肌膚更緊緻、更有光澤；內在，用不含咖啡因的黑膏滋濃縮膠囊，支持穩定、持續的日常活力。',
   situations=['熬夜、壓力大，鏡子裡的自己看起來很累','想找溫和、能長期持續的初老保養','每天靠咖啡撐著，想換一種更穩定的方式'],
   reframe=[('支撐與光澤','人參、當歸、白芍、茯苓、積雪草 × 胜肽、神經醯胺 NP、透明質酸——幫助肌膚看起來更緊緻、更明亮。'),('穩定活力','西洋參、黃芪、山藥等七味草本協同，不靠咖啡因的短暫刺激，支持持續穩定的日常活力。'),('能持續的才算數','早晚使用、每天隨餐——溫和到可以一直用，才是真正會留下來的保養。')],
   products=['lifting-serum','enerbalance'], bundle=None,
   combo=('怎麼搭','精華液早晚擦；EnerBalance 每天 2 次、每次 3 粒隨餐。孕婦、哺乳期、服藥中請先諮詢醫師。'),
   faq=[('精華液男生可以用嗎？','可以。男女適用，35 歲以上尤其合適；質地清爽，早晚潔面後使用。'),('EnerBalance 會像咖啡一樣讓人睡不著嗎？','EnerBalance 不含咖啡因與強刺激性成分，思路是日常滋養而非提神。每個人體質不同，建議隨餐服用並觀察。'),('黑膏滋是什麼？','黑膏滋是傳統的草本膏方；EnerBalance 把它濃縮成膠囊，更方便、更衛生、也更容易每天持續。')],
   photo=shop_img('collections/4_0cd12e86-74cf-4588-b39b-7b5c570db219.jpg?v=1776886625',900), image=f'{IMG}/products/herbal-lifting-revitalizing-serum/lifting-serum-product-shot-wide.png', image_fallback=f'{IMG}/products/herbal-lifting-revitalizing-serum/herbal-lifting-revitalizing-serum-bottle-front.png'),
}
SERIES_ORDER = ['eye','dental','sleep','digestive','skin','vitality']

PRODUCTS = {
 'eye-patches': dict(series='eye', name='WiseQuest 明目冷敷眼貼', en='Herbal Cooling Eye Patches', badge=('badge-star','明星產品'),
   hook='清涼、放鬆，睡飽的雙眼', desc='睡前貼在眼周，草本透過肌膚緩緩釋放，讓長時間用眼後的雙眼在夜裡好好休息。不入眼、不含防腐劑，日本製造。',
   long='一天盯著螢幕十個小時之後，眼睛需要的不只是「這一刻舒服一點」，而是一段真正的休息。明目冷敷眼貼貼在內眼角、外眼角與下眼瞼下方的肌膚上，桉葉、菊花、薄荷、甘草等草本透過肌膚緩緩釋放，在你睡著的時候陪著眼睛。',
   herbs='桉葉、菊花、薄荷、甘草', actives='—（純草本配方）', made='日本製造', form='外用透皮冷敷眼貼', spec='1 盒 10 片；體驗裝 12 片（約兩晚）',
   usage='清潔眼周後，睡前貼於內眼角、外眼角與下眼瞼下方，每次 2–6 片，約 30 分鐘或整晚；早上撕下。', caution='僅供外用；首次使用前先做局部皮膚測試；孕婦請勿使用；如有不適請停止使用。',
   price=29.99, price_note='1 盒 10 片 · 約 10 晚', handle='草本冷敷眼貼-十天包裝-贈試用裝一袋-價值-5',
   variants=[('兩晚體驗裝（12 片）','$6.00','先試再決定',False),('1 盒 · 10 片','$29.99','約 10 晚',False),('3 盒 · 一個月組','$84.00','推薦入門',True),('6 盒 · 兩個月組','$162.00','',False),('9 盒 · 三個月組','$234.00','單片成本最低',False)],
   trial_handle='試用裝-2日份-wise-quest-草本冷敷眼貼',
   yes=['每天盯螢幕超過 8 小時的上班族與學生','睡前習慣滑手機、想讓眼睛好好休息的人','想先用 $6 試兩晚再決定的人'], no=['孕婦','眼周肌膚有傷口或正在發炎者','對配方任一成分過敏者'],
   faq=[('會進到眼睛裡嗎？','不會。眼貼貼在眼周肌膚上，不入眼。日本製造、不含防腐劑，過敏回報極少（依品牌內部客服紀錄）。'),('白天可以用嗎？','可以。白天用 2–4 片做一次螢幕空檔的輕量護理；睡前再貼滿。白天不方便貼時，可以改用草本舒緩修護眼霜。'),('多久會有感覺？','多數人在使用時就能感受到清涼放鬆；整體的舒適感通常隨著幾週的持續使用慢慢累積，效果因人而異。')],
   image=shop_img('files/XXT36515.jpg?v=1781960251'), cross=['lumiview','eye-cream','eye-care-trio']),
 'lumiview': dict(series='eye', name='LumiView 草本明目膠囊', en='Herbal Eye Support Capsules', badge=None,
   hook='由內支持眼睛的長期健康', desc='七種東方養目草本濃縮成膠囊，從營養與整體狀態支持眼睛；搭配眼貼，外內更完整。180 粒／約 1 個月。',
   long='中醫傳統認為「肝開竅於目、肝腎同源」——眼睛的狀態，與身體整體的滋養有關。LumiView 以枸杞、菊花、決明子、山藥、茯苓、當歸、黃芪七味傳統草本，從內在支持眼睛的長期健康，是護眼三寶裡負責「內」的那一件。',
   herbs='枸杞、菊花、決明子、山藥、茯苓、當歸、黃芪（七味）', actives='—（純草本複方）', made='美國製造', form='全植物膠囊（全素）', spec='180 粒／瓶 ≈ 1 個月',
   usage='每天 2 次、每次 3 粒，隨餐服用，作為長期眼部健康管理的一部分。', caution='孕婦、哺乳期、服藥中或有健康疑慮者，使用前請諮詢醫師。',
   price=119, price_note='180 粒 · 約 1 個月', handle='wisquest-草本明目膠囊',
   variants=[('1 瓶','$119','',True),('2 瓶','$226.10','',False),('3 瓶','$303.45','單瓶成本最低',False)], trial_handle=None,
   yes=['已經在用眼貼、想「內外一起」的人','長時間用眼、想從內在支持眼睛長期健康的人','偏好全素、成分公開的草本配方'], no=['孕婦與哺乳期（請先諮詢醫師）','正在服用處方藥者（請先諮詢醫師）','對配方任一成分過敏者'],
   faq=[('和葉黃素可以一起吃嗎？','兩者角度不同。是否同時使用請先與醫師或藥師討論。'),('需要一直吃嗎？','建議至少給自己 4–8 週；狀態穩定後可以鞏固一段時間再停用，之後依需要再開始。'),('素食者可以吃嗎？','可以。全植物膠囊，全素。')],
   image=shop_img('files/ChatGPT_Image_2026_3_29_12_19_42.png?v=1776262574'), cross=['eye-patches','eye-cream','eye-care-trio']),
 'eye-cream': dict(series='eye', name='草本舒緩修護眼霜', en='Herbal Soothing & Repair Eye Cream', badge=('badge-new','新品'),
   hook='看不見的眼貼，白天的眼周呵護', desc='3C 與花粉季節、不方便貼眼貼的時候，隨身為脆弱的眼周肌膚保濕與舒緩。無酒精、無人工香精、無合成色素。',
   long='白天在辦公室不方便貼眼貼，但眼周肌膚一樣需要照顧。這款眼霜以石斛、菊花、決明子、茯苓、當歸根與尤加利葉精油，為脆弱的眼周肌膚做日間的保濕與舒緩，是護眼三寶裡負責「日」的那一件。我們把它定位為護眼，而不是抗老。',
   herbs='石斛、菊花、決明子、茯苓、當歸根、尤加利葉精油', actives='無苯氧乙醇、無化學防腐劑、無人工香精、無合成色素、無酒精', made='原料研發日本・生產灌裝美國', form='外用眼霜', spec='20g / 0.7 oz',
   usage='早晚或白天用眼空檔，取米粒大小輕點眼周，由內向外輕輕按壓至吸收。', caution='僅供外用；避免直接接觸眼睛；開封後建議 6 個月內用完。',
   price=59, price_note='20g / 0.7 oz', handle='wisequest-草本舒緩修護眼霜', variants=None, trial_handle=None,
   yes=['白天長時間用眼、想隨身照顧眼周的人','花粉季節眼周容易乾燥不適的人','搭配眼貼，想把日夜都顧到的人'], no=['眼周肌膚有傷口者','對精油類成分敏感者（先局部測試）'],
   faq=[('可以取代眼貼嗎？','它是白天的接力，不是取代。晚上有時間時仍建議使用眼貼。'),('會不會長脂肪粒？','質地設計為清爽型，每次用量米粒大小即可。若有疑慮請先小範圍測試。'),('男生可以用嗎？','可以，男女適用。')],
   image=shop_img('files/Untitled_design_3924dd0b-b2a7-4689-9fe5-931caa8ffc9a.jpg?v=1781959479'), cross=['eye-patches','lumiview','eye-care-trio']),
 'eye-care-trio': dict(series='eye', name='護眼三寶（眼貼＋LumiView＋眼霜）', en='Eye Care Trio', badge=('badge-star','招牌組合'), is_bundle=True,
   hook='外、內、日夜，一次到位', desc='睡前眼貼從外舒緩、白天眼霜接力、LumiView 從內支持——三個產品不是三個選擇，而是一天二十四小時的三個時段。',
   long='很多顧客從 $6 的眼貼體驗裝開始，用了一陣子之後問我們：「還能多做什麼？」護眼三寶就是答案——不是「買三樣更划算」的折扣語言，而是一套方案的三個部分：夜裡（眼貼）、白天（眼霜）、內在（膠囊）。',
   herbs='眼貼：桉葉、菊花、薄荷、甘草｜LumiView：枸杞、菊花、決明子、山藥、茯苓、當歸、黃芪｜眼霜：石斛、菊花、決明子、茯苓、當歸根', actives='詳見各單品頁', made='眼貼日本製造；膠囊與眼霜美國製造', form='外用眼貼＋全植物膠囊＋外用眼霜', spec='依組合頁選擇 1／2／3 個月方案',
   usage='睡前貼眼貼；每天 2 次各 3 粒 LumiView 隨餐；白天用眼空檔擦眼霜。', caution='孕婦請勿使用眼貼；服藥中請先諮詢醫師再使用膠囊。',
   price=None, price_note='組合價以 zh.uhealthfit.com 護眼三寶頁為準', handle=None, page_url=f'{SHOP}/pages/%E8%AD%B7%E7%9C%BC%E4%B8%89%E5%AF%B6', variants=None, trial_handle='試用裝-2日份-wise-quest-草本冷敷眼貼',
   yes=['已經用過眼貼、想把護眼做完整的人','每天螢幕 10 小時以上、想一次把日夜都顧到的人','重視成分公開與長期習慣的人'], no=['還沒試過眼貼的人——建議先從 $6 體驗裝開始','孕婦與哺乳期（請先諮詢醫師）'],
   faq=[('一定要三樣一起用嗎？','不一定。可以從眼貼開始，再依需要加入膠囊或眼霜；三寶是為了想一次到位的人準備的。'),('三個月方案適合誰？','已經用過一個月、確定適合自己習慣的人。單次購買，沒有訂閱。'),('有免運嗎？','美國地區眼貼訂單滿 $79、其他商品滿 $200 免運；組合訂單依結帳頁顯示為準。')],
   image=f'{IMG}/_optimized/concerns/eye-care-1200.avif', cross=['eye-patches','lumiview','eye-cream']),
 'dentaforte': dict(series='dental', name='DentaForte 草本固齒膠囊', en='Herbal Formula for Teeth & Gum Health', badge=None,
   hook='照顧牙刷到不了的地方', desc='十味傳統草本複方，搭配認真刷牙與定期牙科檢查，作為長期口腔健康管理的一部分。隨餐服用，不必改變原有習慣。',
   long='刷牙、牙線、洗牙負責看得見的表面——這些是每天不能少的基本功。DentaForte 從另一個角度出發：中醫傳統認為「腎主骨，齒為骨之餘」，十味草本從內在支持牙齦與牙齒的日常健康。它不是取代牙醫的東西，而是「刷牙之外、看牙之間」每天做得到的保養。',
   herbs='熟地黃、生地黃、黃芪、五味子、丹參、野菊花等十味草本', actives='—（純草本複方）', made='美國 cGMP 製造', form='全植物膠囊（全素）', spec='180 粒／瓶 ≈ 1 個月',
   usage='每天 2 次、每次 3 粒，隨餐服用；搭配認真刷牙、牙線與定期牙科檢查。', caution='孕婦、哺乳期、服藥中或有慢性健康狀況者，使用前請諮詢醫師。有口腔不適請先就醫。',
   price=269, price_note='180 粒 · 約 1 個月', handle='wisequest-草本固齿胶囊',
   variants=[('1 瓶','$269','',True),('2 瓶','$511.10','',False),('3 瓶','$686','單瓶成本最低',False)], trial_handle=None,
   yes=['35–55 歲、想為牙齦長期健康多做一點的人','替父母準備日常口腔保養的子女','重視成分公開、美國製造的人'], no=['正在接受牙科治療者（請先詢問牙醫）','孕婦、哺乳期（請先諮詢醫師）','對配方任一成分過敏者'],
   faq=[('可以取代看牙醫嗎？','不能。這是膳食補充劑，不是藥品；請持續定期牙科檢查。'),('要吃多久？','建議至少 4–8 週，作為長期管理的一部分；效果因人而異。'),('長輩吃方便嗎？','全植物膠囊、隨餐服用，放在早餐旁邊最容易記得，不需要家人在旁盯著。')],
   image=f'{IMG}/_optimized/products/dentaforte/dentaforte-product-shot-wide-1200.avif', cross=['herbalflow','calmoon','lumiview']),
 'calmoon': dict(series='sleep', name='Calmoon 安睡草本膠囊', en='Herbal Sleep Support Capsules', badge=None,
   hook='白天放鬆，夜裡好眠', desc='不含褪黑素的草本安神配方。午後與睡前各一次，先幫忙放下白天的緊繃，支持自然的睡眠節律。狀態穩定後可停用。',
   long='夜裡難以放鬆，常常不是夜晚的問題，而是白天沒有「下線」。中醫傳統認為「心主神明」——Calmoon 以炒酸棗仁、合歡皮、茯神、百合、刺五加、丹參、夏枯草七味草本，先安撫白天的壓力，支持身體進入夜間的恢復狀態。不含褪黑素，狀態穩定後可以停用。',
   herbs='炒酸棗仁、合歡皮、茯神、百合、刺五加、丹參、夏枯草（七味）', actives='不含褪黑素；配方溫和、狀態穩定後可停用', made='美國製造', form='全植物膠囊（全素）', spec='180 粒／瓶 ≈ 1 個月',
   usage='每天 2 次、每次 3 粒：中午飯後一次、晚飯後或睡前一小時一次。', caution='孕婦、哺乳期、服藥中（尤其是鎮靜或助眠類藥物）者，使用前請諮詢醫師。',
   price=139, price_note='180 粒 · 約 1 個月', handle='wisequest-草本助眠膠囊', variants=None, trial_handle=None,
   yes=['壓力大、晚上腦子停不下來的上班族','想避開褪黑素、怕隔天昏沉的人','希望狀態穩定後可以停用、不想長期依賴的人'], no=['正在服用鎮靜或助眠類藥物者（請先諮詢醫師）','孕婦、哺乳期','對配方任一成分過敏者'],
   faq=[('為什麼中午也要吃？','這個配方照顧的是白天的壓力。中午那一次幫忙放下上午的緊繃，晚上那一次支持自然入睡。'),('不含褪黑素，那它靠什麼？','靠傳統上用於安神放鬆的草本複方，思路是支持身體原本的節律，而不是外力「關機」。'),('多久會有感覺？','多數人在前幾週先感受到放鬆感，節律的穩定通常需要 4–8 週；效果因人而異。')],
   image=shop_img('files/ChatGPTImage2026_6_17_05_36_03.jpg?v=1782815977'), cross=['herbalflow','enerbalance','eye-patches']),
 'herbalflow': dict(series='digestive', name='HerbalFlow 草本潤暢膠囊', en='Herbal Digestive Flow Capsules', badge=None,
   hook='順暢自然，不靠刺激', desc='不含番瀉葉。以火麻仁為核心的六味草本複方，兼顧「潤」與「行氣」，溫和支持腸道的自然節律與餐後的輕盈感。',
   long='不是不通，是通了還是脹——潤腸與行氣是兩件事。HerbalFlow 以火麻仁、萊菔子、厚朴、生地黃、當歸、馬齒莧六味草本，一邊潤養、一邊行氣，中醫傳統說「脾主運化」。不含番瀉葉，設計原則是陪腸道找回節奏，而不是逼它；節律穩定後可以停用。',
   herbs='火麻仁、萊菔子、厚朴、生地黃、當歸、馬齒莧（六味）', actives='不含番瀉葉', made='美國製造', form='全植物膠囊（全素）', spec='180 粒／瓶 ≈ 1 個月',
   usage='每天 2 次、每次 3 粒，隨餐或飯後服用；節律穩定後可鞏固一段時間再停用。', caution='孕婦、哺乳期、服藥中或有腸胃相關健康狀況者，使用前請諮詢醫師；有持續腹痛或出血請直接就醫。',
   price=139, price_note='180 粒 · 約 1 個月', handle='wisequest-草本通氣膠囊', variants=None, trial_handle=None,
   yes=['久坐、外食應酬多的上班族','想找不含番瀉葉、溫和選項的人','希望節律穩定後可以停用的人'], no=['孕婦、哺乳期','有持續腹痛、出血等情況者（請先就醫）','對配方任一成分過敏者'],
   faq=[('會不會越吃越多？','HerbalFlow 不含番瀉葉等刺激性成分，設計原則是支持節律；節律穩定後可以停用。'),('和益生菌衝突嗎？','角度不同。是否同時使用請先與醫師或藥師討論。'),('多久會有感覺？','多數人在前幾週先感受到餐後的輕盈感，節律的穩定通常需要 4–8 週；效果因人而異。')],
   image=shop_img('files/26ffef70cacb47ecb0b0b1e2fc667031_3eb53544-8644-47c2-85e1-519efa90b88c.jpg?v=1782815981'), cross=['calmoon','dentaforte','enerbalance']),
 'soothing-cream': dict(series='skin', name='草本舒緩修護霜', en='Herbal Soothing & Repair Cream', badge=('badge-star','家庭必備'),
   hook='家庭必備的無類固醇修護霜', desc='七種草本＋透明質酸、維生素 E，為乾燥脫皮、換季敏感、曬後與蚊蟲叮咬後的肌膚舒緩保濕、強韌屏障。全身可用，早晚各一次。',
   long='一罐放在家裡、全家都用得到的霜：乾燥脫皮時、換季肌膚敏感時、曬後、蚊蟲叮咬後。蒲公英、紫草、白芷、積雪草、苦參、尤加利、薄荷七種草本，加上透明質酸、維生素 E 與維生素 C 衍生物，做的是舒緩、保濕與屏障保養——無類固醇，溫和到可以天天用。',
   herbs='蒲公英、紫草、白芷、積雪草、苦參、尤加利、薄荷（七種）', actives='透明質酸、維生素 E、維生素 C 衍生物；無類固醇', made='美國製造', form='外用霜', spec='全身可用',
   usage='每天 2 次，取適量塗抹於需要保養的部位；首次使用先在小範圍局部測試。', caution='僅供外用；避開眼睛與傷口；若醫師已開立外用藥，請依醫囑使用，不要自行替換。',
   price=69, price_note='外用霜 · 全家可用', handle='wisequest-草本舒緩修護霜', variants=None, trial_handle=None,
   yes=['換季時肌膚容易敏感、乾燥脫皮的人','想找一罐全家可用的無類固醇舒緩霜','曬後、蚊蟲叮咬後需要舒緩保濕的人'], no=['對配方任一成分（含精油類）過敏者','有開放性傷口的部位'],
   faq=[('小孩可以用嗎？','設計為全家可用；嬰幼兒或特殊膚況者請先諮詢醫師並先小範圍測試。'),('可以擦臉嗎？','可以，全身可用；臉部建議先局部測試。'),('和淨顏霜怎麼分？','乾燥、敏感、曬後 → 舒緩修護霜；易出油、容易長痘 → 淨顏霜。可依部位分開使用。')],
   image=shop_img('files/PicCopilot_image2.jpg?v=1776249690'), cross=['clarifying-cream','eye-cream','lifting-serum']),
 'clarifying-cream': dict(series='skin', name='草本淨顏霜', en='Herbal Clarifying Cream', badge=None,
   hook='為易長痘肌膚精選的草本', desc='溫和調理油脂、支持肌膚屏障，讓膚況看起來更勻淨、更安定。搭配清淡飲食與規律作息，一起把肌膚帶回平衡。',
   long='容易出油、容易長痘的膚況，往往一邊壓油、一邊屏障又變得脆弱。草本淨顏霜以蒲公英、金銀花、丹參、黨參、紫草根油，搭配維生素 C 衍生物與視黃醇棕櫚酸酯，一邊調理油脂、一邊支持屏障，讓膚況看起來更勻淨、更安定。',
   herbs='蒲公英、金銀花、丹參、黨參、紫草根油', actives='維生素 C 衍生物、視黃醇棕櫚酸酯', made='美國製造', form='外用霜', spec='臉部日常保養',
   usage='潔面後取適量塗抹於易出油部位，早晚各一次；搭配清淡飲食、忌辛辣油膩。', caution='僅供外用；首次使用先局部測試；若同時使用高濃度 A 醇類產品請留意耐受；大面積或疼痛硬塊請就醫。',
   price=69, price_note='外用霜', handle='wisequest-草本淨顏霜', variants=None, trial_handle=None,
   yes=['容易出油、容易長痘的膚況','想一起照顧油脂與屏障的人','偏好草本、溫和日常保養的人'], no=['對配方任一成分過敏者','大面積或反覆疼痛硬塊者（請先看皮膚科醫師）'],
   faq=[('多久能看到變化？','膚況的安定需要時間，建議至少 4–8 週並搭配作息與飲食；效果因人而異。'),('可以全臉用嗎？','可以，也可以只用於易出油部位，其他部位搭配舒緩修護霜。'),('白天用需要防曬嗎？','建議白天搭配防曬，這是所有臉部保養的基本。')],
   image=shop_img('files/Untitled_design_c0b7bac5-b45b-48f9-bb62-96d6d17052a5.jpg?v=1781960121'), cross=['soothing-cream','lifting-serum','eye-cream']),
 'lifting-serum': dict(series='vitality', name='草本煥顏提升精華液', en='Herbal Lifting & Revitalizing Serum', badge=('badge-star','精選'),
   hook='更緊緻、更有光澤的肌膚', desc='五種東方草本 × 胜肽、神經醯胺 NP、透明質酸，日復一日幫助肌膚看起來更緊緻、更明亮。男女適用，35 歲以上尤其合適。',
   long='你要的不是變年輕，是不要看起來很累。人參、當歸、白芍、茯苓、積雪草五種東方草本，加上胜肽、神經醯胺 NP 與透明質酸，從支撐、屏障、保濕多個面向，幫助肌膚看起來更緊緻、更有光澤——溫和到可以一直用，能持續的才是會留下來的保養。',
   herbs='人參、當歸、白芍、茯苓、積雪草（五種）', actives='胜肽、神經醯胺 NP、透明質酸', made='美國製造', form='外用精華液', spec='早晚使用',
   usage='潔面後取 2–3 滴，輕拍全臉至吸收，早晚各一次；後續可疊加保濕。', caution='僅供外用；首次使用先局部測試；白天建議搭配防曬。',
   price=189, price_note='精華液', handle='wisequest-草本煥顏提升精華液', variants=None, trial_handle=None,
   yes=['35 歲以上、熬夜壓力大、不想看起來很累的人','想找溫和、能長期持續的初老保養','男女皆適用'], no=['對配方任一成分過敏者','肌膚有傷口或正在發炎的部位'],
   faq=[('和 A 醇類精華比呢？','各有定位。這款走東方草本 × 胜肽的溫和路線，適合想長期持續使用的人。'),('多久有感？','光澤感通常先出現，緊緻感需要更長時間累積；效果因人而異。'),('可以和眼霜一起用嗎？','可以。眼周建議用草本舒緩修護眼霜，全臉用精華液。')],
   image=shop_img('files/1_9cefe0d6-9848-412c-98c1-462e0c23660b.png?v=1782816030'), cross=['eye-cream','soothing-cream','enerbalance']),
 'enerbalance': dict(series='vitality', name='EnerBalance 黑膏滋膠囊', en='Herbal Vitality Capsules', badge=('badge-new','現貨'), compare=299,
   hook='不靠咖啡因，日日滋養', desc='傳統黑膏滋濃縮成膠囊。七味草本協同配方，支持穩定、持續的日常活力；不含咖啡因與強刺激性成分，無麩質、無添加糖。',
   long='咖啡因給的是短暫的提神，而且常常要付出隔天的代價。EnerBalance 把傳統黑膏滋濃縮成膠囊：西洋參、黃芪、山藥、當歸、陳皮、菊花、玉米鬚七味草本協同，中醫傳統認為可用於日常調養，支持穩定、持續的活力。不含咖啡因，無麩質、無添加糖。',
   herbs='西洋參、黃芪、山藥、當歸、陳皮、菊花、玉米鬚（七味）', actives='不含咖啡因與強刺激性成分；無麩質、無添加糖', made='美國製造', form='全植物膠囊', spec='180 粒／瓶 ≈ 1 個月',
   usage='成人每天 2 次、每次 3 粒，建議隨餐服用。', caution='孕婦、哺乳期、服藥中或有慢性健康狀況者，使用前請諮詢醫師。',
   price=179, price_note='180 粒 · 約 1 個月 · 原價 $299', handle='wisequest-黑膏滋膠囊', variants=None, trial_handle=None,
   yes=['工作壓力大、常覺得精力不足的成年人','想減少對咖啡因依賴的人','重視天然草本日常調養的人'], no=['孕婦、哺乳期','正在服用處方藥者（請先諮詢醫師）','18 歲以下'],
   faq=[('會像咖啡一樣讓人睡不著嗎？','不含咖啡因與強刺激性成分，思路是日常滋養而非提神；建議隨餐服用並觀察。'),('黑膏滋是什麼？','傳統的草本膏方，EnerBalance 把它濃縮成膠囊，更方便、更衛生。'),('現在的價格是多少？','商店目前以 $179 供應（原價 $299），實際金額以 zh.uhealthfit.com 結帳頁顯示為準。')],
   image=f'{IMG}/_optimized/products/enerbalance/enerbalance-product-shot-wide-1200.avif', cross=['calmoon','herbalflow','lifting-serum']),
}
PRODUCT_ORDER = ['eye-patches','lumiview','eye-cream','eye-care-trio','dentaforte','calmoon','herbalflow','soothing-cream','clarifying-cream','lifting-serum','enerbalance']

# 部落格
POSTS = []
for fn in sorted(os.listdir(os.path.join(ROOT,'posts'))):
    s = open(os.path.join(ROOT,'posts',fn),encoding='utf8').read()
    meta, body = s.split('---END-META---',1)
    m = json.loads(meta.strip()); m['body'] = body.strip(); POSTS.append(m)
POST_BY_SLUG = {p['slug']:p for p in POSTS}
POST_ORDER = ['eye-patch-vs-steam-mask-vs-eye-drops','beyond-lutein-eye-care','melatonin-free-sleep-aid-guide','stress-daytime-relax-night-sleep','gentle-digestive-support-no-senna','bloating-after-sitting-herbal-flow','gum-care-supplement-for-parents','brushing-plus-herbal-support','steroid-free-soothing-cream-guide','acne-prone-skin-herbal-cream-guide','anti-fatigue-look-serum-guide','caffeine-free-energy-herbal-guide']
POSTS = [POST_BY_SLUG[s] for s in POST_ORDER]

# ───────────────────────────── 共用片段 ─────────────────────────────
def esc(s): return H.escape(s, quote=True)

def buy_url(p, slug):
    if p.get('page_url'): return p['page_url']
    return shop_url(p['handle'])

def price_str(p, with_compare=False):
    if p['price'] is None: return '組合價'
    v = p['price']; base = f'${v:,.2f}' if v != int(v) else f'${int(v)}'
    if with_compare and p.get('compare'):
        c = p['compare']; cs = f'${c:,.2f}' if c != int(c) else f'${int(c)}'
        return f'{base} <s style="color:var(--ink-3);font-weight:600;font-size:.7em;margin-left:6px">{cs}</s>'
    return base


# ───── 產品頁「主題花體字」橫幅：取自 uhealthfit.com/zh-TW 首頁輪播（花體字 SVG、簡介、底色）─────
SLIDES = {
 'eye-patches':      dict(svg='eye-patches',         bg='#D9E2EE', headline='清涼 放鬆／睡飽的雙眼',        intro='日本製冷敷眼貼——休息時貼上，給盯了一整天螢幕的雙眼一份草本呵護。', shot='eye-patches/eye-patches-box-front', avif=False),  # 此圖的 avif 版本沒有透明背景，只用 PNG
 'lumiview':         dict(svg='herbalflow-capsules', bg='#D6DEC7', headline='草本濃縮進膠囊／搭配眼貼更完整', intro='七味東方養目草本濃縮成膠囊，從內在支持眼睛的長期健康；搭配眼貼，外內更完整。', shot='lumiview/lumiview-product-shot-wide'),
 'eye-cream':        dict(svg='eye-patches-3c',      bg='#F8F2E8', headline='看不見的眼貼／3C 花粉 全呵護',   intro='為脆弱眼周設計的植萃眼霜——不便使用眼貼時的隨身養護。', shot='herbal-soothing-repair-eye-cream/eye-cream-product-shot-wide'),
 'dentaforte':       dict(svg='dentaforte',          bg='#F2DCB4', headline='健康牙齦／穩固牙齒',            intro='每日草本膠囊，由內支持牙齦與牙齒——照顧牙刷到不了的深處。', shot='dentaforte/dentaforte-product-shot-wide'),
 'calmoon':          dict(svg='calmoon',             bg='#C8D9F3', headline='白天放鬆／夜裡好眠',            intro='草本安神配方——睡前慢慢放鬆，自然入睡。', shot='calmoon/calmoon-product-shot-wide'),
 'herbalflow':       dict(svg='herbalflow',          bg='#E4EBDD', headline='通腹順暢自然／不靠刺激',        intro='以火麻仁為核心的草本複方，溫和支持腸道自然節律。', shot='herbalflow/herbalflow-product-shot-wide'),
 'soothing-cream':   dict(svg='calming',             bg='#F2DDC6', headline='鎮靜 舒適／更柔軟的肌膚',        intro='不含刺激性活性成分的植萃修護，為乾燥與壓力肌帶來每日的溫和呵護。', shot='herbal-soothing-repair-cream/soothing-repair-cream-product-shot-wide'),
 'clarifying-cream': dict(svg='clarifying-cream',    bg='#F6E9D9', headline='為易長痘肌膚／精選的草本',      intro='溫和淨顏的植萃面霜，讓膚色看起來更勻淨、更安定。', shot='herbal-clarifying-cream/clarifying-cream-product-shot-wide'),
 'lifting-serum':    dict(svg='lifting-serum',       bg='#D3CFAD', headline='更緊緻 更亮澤／更年輕的肌膚',    intro='高濃度植萃精華，日復一日，見證肌膚的提升與煥亮。', shot='herbal-lifting-revitalizing-serum/lifting-serum-product-shot-wide'),
 'enerbalance':      dict(svg='enerbalance',         bg='#ECE4D4', headline='咖啡因短暫提神／不如日日滋養',    intro='真正持久的活力，來自身體整體協調。戒掉咖啡因，不用再靠刺激。', shot='enerbalance/enerbalance-product-shot-wide'),
}
def series_hero(k, rel):
    """系列頁頁首輪播：同 uhealthfit.com/zh-TW 首頁 slides——滿版、左文右圖、自動切換。
    第一張是系列介紹（含 h1），後面每個產品一張（花體字標題）。"""
    s=SERIES[k]; guide=[p for p in POSTS if p['series']==k][0]['slug']
    slides=[f'''<article class="slide slide-intro" aria-label="{esc(s['name'])}">
    <div class="wrap slide-inner">
      <div class="slide-text"><div class="crumbs"><a href="{rel}index.html">首頁</a><span>›</span><span>六大系列</span><span>›</span><span>{s['name']}</span></div>
        <span class="series-tag s-{k}"><span class="dot"></span>{s['name']} · {esc(s['tag'])}</span>
        <h1>{esc(s['h1'])}</h1><p class="lead">{esc(s['lead'])}</p>
        <div class="hero-cta"><a class="btn btn-primary" href="#products">看這個系列的產品</a><a class="btn btn-ghost" href="{rel}blog/{guide}.html">先讀選購指南</a></div>
        <ul class="hero-trust"><li>{esc(s['organ'])}（中醫傳統觀點）</li><li>成分全部公開</li><li>效果因人而異，誠實交代時間</li></ul></div>
      <div class="slide-photo"><img src="{s['photo']}" alt="{esc(s['name'])}" width="900" height="900" fetchpriority="high"></div>
    </div>
  </article>''']
    for slug in s['products']:
        sl=SLIDES.get(slug); p=PRODUCTS[slug]
        if not sl: continue
        avif='' if sl.get('avif') is False else f'<source srcset="{IMG}/_optimized/products/{sl["shot"]}-1200.avif" type="image/avif">'
        slides.append(f'''<article class="slide" style="--slide-bg:{sl['bg']}" aria-label="{esc(p['name'])}">
    <div class="wrap slide-inner">
      <div class="slide-text">
        <div class="slide-name">WISEQUEST {esc(p['name'].replace('WiseQuest ',''))}</div>
        <img class="slide-title" src="{IMG}/home/hero-title-{sl['svg']}-zh-hant.svg" alt="{esc(sl['headline'])}" loading="lazy">
        <p class="slide-intro-text">{esc(sl['intro'])}</p>
        <p class="slide-herbs">主要成分：{esc(p['herbs'])}</p>
        <div class="hero-cta"><a class="btn btn-primary ext" data-product="{slug}" href="{buy_url(p,slug)}">立即選購</a><a class="btn btn-ghost" href="{rel}products/{slug}.html">了解產品</a></div>
      </div>
      <div class="slide-pic"><picture>{avif}<img src="{IMG}/products/{sl['shot']}.png" alt="{esc(p['name'])}" loading="lazy"></picture></div>
    </div>
  </article>''')
    cur_attr=' aria-current="true"'
    dots=''.join(f'<button type="button" aria-label="前往第 {i+1} 張"{cur_attr if i==0 else ""}></button>' for i in range(len(slides)))
    return f'''<section class="slides" aria-roledescription="carousel" aria-label="{esc(s['name'])}">
  <div class="slides-track">{''.join(slides)}</div>
  <button type="button" class="slides-prev" aria-label="上一張">‹</button><button type="button" class="slides-next" aria-label="下一張">›</button>
  <div class="slides-dots">{dots}</div>
</section>
'''

def og_png(url):
    # 社群分享預覽不支援 AVIF：把 uhealthfit.com 的 _optimized/...-1200.avif 換回原始 PNG
    m=re.match(r'(https://uhealthfit\.com)/_optimized/(.+)-\d+\.avif$', url)
    return f'{m.group(1)}/{m.group(2)}.png' if m else url

def head(title, desc, rel, canonical_path, page_id, og_image=None, extra=''):
    return f'''<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{SITE_URL}/{canonical_path}">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{og_png(og_image) if og_image else IMG + '/home/all-products-lineup.png'}">
<meta property="og:locale" content="zh_TW">
<link rel="icon" href="{LOGO}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@500;600;700;800&family=Noto+Sans+TC:wght@400;500;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{rel}css/style.css?v={CSS_VER}">
{extra}
<!-- 上線前：在此插入 GTM / GA4 / Meta Pixel 容器 -->
</head>
<body data-page="{page_id}">
'''

def nav(rel, active=''):
    dd = ''.join(f'<a class="s-{k}" href="{rel}series/{k}.html"><span class="dot"></span><span>{SERIES[k]["name"]}<small>{SERIES[k]["h1"]}</small></span></a>' for k in SERIES_ORDER)
    mob_sub = ''.join(f'<a href="{rel}series/{k}.html">{SERIES[k]["name"]}</a>' for k in SERIES_ORDER)
    def a(href,label,key):
        cls = ' class="active"' if active==key else ''
        return f'<a href="{href}"{cls}>{label}</a>'
    return f'''<div class="topbar">美國地區：眼貼滿 <b>USD $79</b>、其他商品滿 <b>USD $200</b> 免運 · 30 天內未拆封可退 · 於 zh.uhealthfit.com 安全結帳</div>
<header class="nav">
  <div class="wrap">
    <a class="brand" href="{rel}index.html" aria-label="優健堂 UHealthFit 首頁"><img src="{LOGO}" alt="優健堂 UHealthFit" width="101" height="34"></a>
    <nav aria-label="主選單"><ul class="nav-links">
      <li>{a(rel+'series/eye.html','六大系列','series')}<div class="dd">{dd}</div></li>
      <li>{a(rel+'blog/index.html','選購指南','blog')}</li>
      <li>{a(rel+'quiz.html','30 秒測驗','quiz')}</li>
      <li>{a(rel+'about.html','關於與黃醫師','about')}</li>
      <li>{a(rel+'faq.html','常見問題','faq')}</li>
    </ul></nav>
    <div class="nav-cta"><a class="btn btn-primary btn-sm" href="{rel}series/eye.html">選購系列</a><button class="menu-btn" aria-label="開啟選單" aria-expanded="false"><span></span></button></div>
  </div>
  <div class="mobile-menu"><div class="wrap">
    <a href="{rel}index.html">首頁</a>
    <a href="{rel}series/eye.html">六大系列</a><div class="sub">{mob_sub}</div>
    <a href="{rel}blog/index.html">選購指南</a><a href="{rel}quiz.html">30 秒測驗</a><a href="{rel}about.html">關於與黃醫師</a><a href="{rel}faq.html">常見問題</a>
  </div></div>
</header>
<main>
'''

def journey(rel, stage, series_key=None, post=None, product=None):
    """客戶旅程「下一步」模組。stage: home / series / product / blog / quiz / about"""
    cards = []
    if stage in ('home','about','faq'):
        cards.append(('STEP 1','還不確定從哪裡開始？','6 題、30 秒，找到最值得先照顧的那一件事，並對應到系列與選購指南。',f'{rel}quiz.html','開始 30 秒測驗'))
        cards.append(('STEP 2','先讀一篇選購指南','我們把每個系列「怎麼選」寫成指南——就算不買，也能更懂自己的身體。',f'{rel}blog/index.html','看選購指南'))
    elif stage=='series' and series_key:
        posts=[p for p in POSTS if p['series']==series_key]
        cards.append(('讀一讀','這個系列怎麼選',posts[0]['excerpt'],f'{rel}blog/{posts[0]["slug"]}.html','閱讀指南'))
        cards.append(('不確定？','30 秒找到起點','如果你同時在意好幾件事，先做測驗，我們幫你排序。',f'{rel}quiz.html','開始測驗'))
    elif stage=='blog' and post:
        p=PRODUCTS[post['primary_product']]
        cards.append(('下一步','看對應產品',p['hook']+'——'+p['desc'][:40]+'…',f'{rel}products/{post["primary_product"]}.html','查看產品'))
        cards.append(('或是','30 秒測驗','不只在意這一件事？先做測驗，找到最值得先開始的系列。',f'{rel}quiz.html','開始測驗'))
    elif stage=='product' and product:
        sk=PRODUCTS[product]['series']; posts=[p for p in POSTS if p['series']==sk]
        cards.append(('延伸閱讀',posts[0]['title'][:22]+('…' if len(posts[0]['title'])>22 else ''),posts[0]['excerpt'],f'{rel}blog/{posts[0]["slug"]}.html','閱讀指南'))
        cards.append(('看整個系列',SERIES[sk]['name'],SERIES[sk]['lead'][:48]+'…',f'{rel}series/{sk}.html','前往系列頁'))
    elif stage=='quiz':
        cards.append(('不想測？','直接看六大系列','從最在意的那一件事開始，每個系列都可以單獨開始。',f'{rel}series/eye.html','看六大系列'))
        cards.append(('先讀一篇','選購指南','每個系列的「怎麼選」都寫成了指南。',f'{rel}blog/index.html','看選購指南'))
    html_cards=''.join(f'<div class="jcard"><div class="k">{k}</div><h3>{esc(t)}</h3><p>{esc(d)}</p><a class="btn btn-ghost btn-sm" href="{h}">{b}</a></div>' for k,t,d,h,b in cards)
    return f'''<section class="sec-tight journey"><div class="wrap">
  <div class="lead-box"><span class="eyebrow">你的下一步</span><h2>開始，比完美更重要</h2><p class="lead" style="font-size:16px">養護是累積出來的。從一件小事開始，剩下的我們陪你慢慢來。</p></div>
  {html_cards}
</div></section>
'''

def disclaimer():
    return '''<section class="disclaimer" aria-label="免責聲明"><div class="wrap">
<p><b>免責聲明：</b>本站所述膠囊類產品為膳食補充劑，乳霜、精華液與眼貼為日常保養用品，皆非藥品。相關敘述未經美國食品藥物管理局（FDA）評估；本產品不用於診斷、治療、治癒或預防任何疾病。「生產設施具 FDA 登記」指設施登記資訊，不代表 FDA 核准或背書任何產品。</p>
<p>These statements have not been evaluated by the Food and Drug Administration. These products are not intended to diagnose, treat, cure, or prevent any disease.</p>
<p>本站資訊僅供參考，不可取代醫師或其他專業醫療人員的建議；請勿依據本站內容自行診斷或處理任何健康問題。若有或疑似有任何健康問題，請諮詢你的醫療照護人員。使用者分享與買家評價皆為個人經驗，效果因人而異。孕婦、哺乳期、18 歲以下、服藥中或有慢性健康狀況者，使用前請先諮詢醫師。中醫相關敘述為傳統觀點的說明，非醫療診斷。部分情境圖片可能為示意圖；實際包裝可能與圖片略有差異。所有購買於 zh.uhealthfit.com 完成，價格以結帳頁顯示為準。</p>
</div></section>
'''

def footer(rel):
    series_links=''.join(f'<li><a href="{rel}series/{k}.html">{SERIES[k]["name"]}</a></li>' for k in SERIES_ORDER)
    pays=''.join(f'<img src="{IMG}/payment/{p}.svg" alt="{p}">' for p in ['visa','mastercard','american-express','discover','apple-pay','google-pay','shop-pay'])
    return f'''</main>
{disclaimer()}
<footer class="site"><div class="wrap">
  <div><img class="logo" src="{rel}{LOGO_WHITE}" alt="UHealthFit" width="146" height="26"><p>融合傳統智慧與現代科學的健康養護平台。</p><p style="margin-top:10px">Uhealth Trading Inc.<br>90 North St, Suite D, Middletown, NY 10940, USA<br><a href="mailto:service@uhealthfit.com">service@uhealthfit.com</a></p><div class="pay">{pays}</div></div>
  <div><h4>六大系列</h4><ul>{series_links}</ul></div>
  <div><h4>探索</h4><ul><li><a href="{rel}blog/index.html">選購指南</a></li><li><a href="{rel}quiz.html">30 秒測驗</a></li><li><a href="{rel}about.html">關於優健堂與黃醫師</a></li><li><a href="{rel}faq.html">常見問題</a></li><li><a href="{rel}products/eye-care-trio.html">護眼三寶</a></li></ul></div>
  <div><h4>購買與客服</h4><ul><li><a class="ext" href="{SHOP}">前往 zh.uhealthfit.com 商店</a></li><li><a class="ext" href="{SHOP}/policies/shipping-policy">運送說明</a></li><li><a class="ext" href="{SHOP}/policies/refund-policy">退貨政策</a></li><li><a class="ext" href="{SHOP}/policies/privacy-policy">隱私權政策</a></li><li><a class="ext" href="{SHOP}/policies/terms-of-service">服務條款</a></li></ul></div>
  <div class="copy">© 2026 Uhealth Trading Inc. 版權所有。本站為 WiseQuest 系列的介紹網站，購買於 zh.uhealthfit.com 完成。</div>
</div></footer>
<script src="{rel}js/main.js?v={JS_VER}" defer></script>
</body></html>
'''

def sticky(rel):
    return f'<div class="sticky-cta" aria-label="快速行動"><a class="btn btn-ghost" href="{rel}quiz.html">30 秒測驗</a><a class="btn btn-primary" href="{rel}series/eye.html">選購系列</a></div>'

def product_card(slug, rel, wide=False):
    p=PRODUCTS[slug]
    badge=f'<span class="badge {p["badge"][0]}">{p["badge"][1]}</span>' if p.get('badge') else ''
    pr = price_str(p); note=p['price_note']
    return f'''<article class="prod{' wide' if wide else ''}">
  <a class="pic" href="{rel}products/{slug}.html">{badge}<img src="{p['image']}" alt="{esc(p['name'])}" loading="lazy"></a>
  <div class="body">
    <div class="name"><a href="{rel}products/{slug}.html">{esc(p['name'])}</a><small>{esc(p['en'])} · {esc(p['made'])}</small></div>
    <div class="hook">{esc(p['hook'])}</div>
    <p class="desc">{esc(p['desc'])}</p>
    <p class="herbs"><b>主要成分：</b>{esc(p['herbs'])}</p>
    <div class="foot"><div class="price">{pr}<small>{esc(note)}</small></div><div style="display:flex;gap:8px"><a class="btn btn-ghost btn-sm" href="{rel}products/{slug}.html">了解</a><a class="btn btn-primary btn-sm ext" data-product="{slug}" href="{buy_url(p,slug)}">購買</a></div></div>
  </div>
</article>'''

def post_card(p, rel):
    prod=PRODUCTS[p['primary_product']]; s=SERIES[p['series']]
    same=[q for q in POSTS if q['series']==p['series']]
    thumb = s['photo'] if same.index(p)%2==0 else prod['image']  # 同系列第一篇用情境照、第二篇用產品實拍，避免縮圖重複
    return f'''<article class="post-card s-{p['series']}" data-series="{p['series']}">
  <a class="thumb" href="{rel}blog/{p['slug']}.html"><img src="{thumb}" alt="" loading="lazy"></a>
  <div class="body"><div class="meta"><span class="series-tag s-{p['series']}"><span class="dot"></span>{s['name']}</span><span>· 約 {p['reading_min']} 分鐘</span></div>
  <h3><a href="{rel}blog/{p['slug']}.html">{esc(p['title'])}</a></h3><p>{esc(p['excerpt'])}</p>
  <a class="go" style="color:var(--green);font-weight:700;font-size:14px" href="{rel}blog/{p['slug']}.html">閱讀指南 →</a></div>
</article>'''

def faq_block(items):
    return ''.join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q,a in items)

def faq_ld(items):
    return json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in items]},ensure_ascii=False)

def externalize(content):
    # 所有連到 zh.uhealthfit.com 的連結另開新分頁，讓使用者能回到本站
    def fix(m):
        tag=m.group(0)
        if 'target=' in tag: return tag
        return tag[:-1]+' target="_blank" rel="noopener">'
    return re.sub(r'<a\s[^>]*href="https://zh\.uhealthfit\.com[^"]*"[^>]*>', fix, content)

def write(path, content):
    full=os.path.join(DIST,path); os.makedirs(os.path.dirname(full),exist_ok=True)
    if path.endswith('.html'): content=externalize(content)
    open(full,'w',encoding='utf8').write(content)

# ───────────────────────────── 首頁 ─────────────────────────────
def build_home():
    rel=''
    series_cards=''.join(f'''<a class="scard s-{k}" href="series/{k}.html"><div class="scard-pic"><img src="{SERIES[k]['photo']}" alt="" loading="lazy"></div><span class="series-tag"><span class="dot"></span>{SERIES[k]['en']}</span><h3>{SERIES[k]['name']}</h3><div class="hook">{SERIES[k]['h1']}</div><p>{esc(SERIES[k]['lead'][:60])}…</p><div class="items">{'・'.join(PRODUCTS[s]['name'].replace('WiseQuest ','') for s in SERIES[k]['products'])}</div><span class="go">看系列 →</span></a>''' for k in SERIES_ORDER)
    posts=''.join(post_card(p,rel) for p in [POST_BY_SLUG[s] for s in ['eye-patch-vs-steam-mask-vs-eye-drops','melatonin-free-sleep-aid-guide','gum-care-supplement-for-parents']])
    featured=''.join(product_card(s,rel) for s in ['eye-patches','calmoon','dentaforte'])
    body=f'''
<section class="hero"><div class="wrap">
  <div><span class="eyebrow">優健堂 UHealthFit × WiseQuest · 醫師研發草本保健</span>
    <h1>不壓制、不依賴，<br><em>從根源支持身體</em></h1>
    <p class="lead">護眼、固齒、舒眠、順暢、肌膚、活力——六大日常養護系列，由中國中西醫結合執業醫師黃醫師研發。傳統草本配方、現代萃取工藝，美國・日本製造，成分全部公開。</p>
    <div class="hero-cta"><a class="btn btn-primary" href="quiz.html">30 秒找到我的起點</a><a class="btn btn-ghost" href="series/eye.html">直接看六大系列</a></div>
    <ul class="hero-trust"><li>無添加 · 非轉基因</li><li>第三方純度檢測</li><li>全植物膠囊 · 全素</li></ul>
  </div>
  <div class="hero-visual cutout"><picture><source type="image/avif" srcset="{IMG}/_optimized/all-products-product-shot-wide-800.avif 800w, {IMG}/_optimized/all-products-product-shot-wide-1200.avif 1200w, {IMG}/_optimized/all-products-product-shot-wide-1448.avif 1448w" sizes="(max-width:900px) 100vw, 600px"><source type="image/webp" srcset="{IMG}/_optimized/all-products-product-shot-wide-800.webp 800w, {IMG}/_optimized/all-products-product-shot-wide-1200.webp 1200w, {IMG}/_optimized/all-products-product-shot-wide-1448.webp 1448w" sizes="(max-width:900px) 100vw, 600px"><img src="{IMG}/all-products-product-shot-wide.png" alt="WiseQuest 全系列產品，膠囊瓶、乳霜罐、精華液與眼貼盒" width="1448" height="1086" fetchpriority="high"></picture></div>
</div></section>
<section class="trustbar" aria-label="品質保證"><div class="wrap"><ul>
  <li>美國・日本製造<small>cGMP 規範生產</small></li><li>第三方純度檢測<small>成品送驗</small></li><li>成分全部公開<small>每一味都查得到</small></li><li>無添加 · 非轉基因<small>無人工色素、防腐劑</small></li><li>執業醫師研發<small>二十年臨床經驗</small></li><li>30 天未拆封可退<small>service@uhealthfit.com</small></li>
</ul></div></section>

<section class="sec"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">六大系列 · 11 款產品</span><h2>從最在意的那一件事開始</h2><p class="lead">每個系列都可以單獨開始，也可以彼此搭配。點進系列頁，看怎麼選、怎麼用、怎麼開始。</p></div>
  <div class="grid-3">{series_cards}</div>
</div></section>

<section class="sec bg-cream"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">為什麼是草本日常養護</span><h2>現代生活，常常把身體排在最後</h2><p class="lead">一天盯螢幕十個小時、晚睡、外食、壓力停不下來——身體會用各種小訊號提醒我們。即時舒緩很重要；但長期的日常養護，是另一件值得開始的事。</p></div>
  <div class="grid-3">
    <div class="card white"><div class="num">01</div><h3>訊號，不只是訊號</h3><p>長時間用眼後的乾澀疲勞感、換季時容易敏感的肌膚、難以放鬆的夜晚、久坐後的腹脹——它們往往是生活型態累積出來的結果。</p></div>
    <div class="card white"><div class="num">02</div><h3>舒緩當下，也要照顧長期</h3><p>市面上多數方案專注於「這一刻舒服一點」。我們尊重這些選擇，也認為日常養護值得有自己的位置。</p></div>
    <div class="card white"><div class="num">03</div><h3>一套邏輯，六個系列</h3><p>以中醫的整體觀看待身體，用傳統使用數百年的草本、搭配現代萃取與品質檢測，把「日常養護」做成每天做得到的小習慣。</p></div>
  </div>
  <div class="pull">「身體一直在努力照顧你。現在，換我們照顧它。」<small>WiseQuest 品牌理念 · 草本是支持，不是取代身體；我們尊重現代醫學，也珍惜傳統草本智慧。</small></div>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">常見的起點</span><h2>三個常見的起點</h2></div>
  <div class="pgrid">{featured}</div>
</div></section>

<section class="sec bg-green-light"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">選購指南</span><h2>先懂怎麼選，再決定要不要買</h2><p class="lead">我們把每個系列「市面上有哪些選項、各自負責什麼、選購時該看什麼」寫成指南。就算最後沒有購買，也希望你更懂自己的身體。</p></div>
  <div class="bgrid">{posts}</div>
  <p style="margin-top:22px"><a class="btn btn-ghost" href="blog/index.html">看全部 12 篇選購指南</a></p>
</div></section>

<section class="sec doctor bg-dark"><div class="wrap">
  <div><img src="{IMG}/home/dr-h.png" alt="黃醫師 Dr. Huang，中國中西醫結合執業醫師" loading="lazy"></div>
  <div><span class="eyebrow">研發者 · 黃醫師 Dr. Huang</span><h2>由一位看了二十年「整個人」的醫師研發</h2>
  <p>黃醫師是中國中西醫結合執業醫師、中醫全科醫師，擁有二十年臨床經驗與草本配方研發專長。她師從多位國家級名老中醫、各科教授與清末御醫傳人；臨床涉及內科、皮膚科、婦科、兒科，並專研中醫美容二十年，自主研發的中藥化妝品曾獲國家發明專利。</p>
  <blockquote>「很多時候讓症狀暫時消失，不等於身體真的恢復。我想做的，是幫身體重新找回自己健康的狀態——用承傳千年的草本經驗，幫助身體恢復平衡。」<footer>— 黃醫師 · WiseQuest 配方研發者</footer></blockquote>
  <a class="btn btn-light" href="about.html">認識黃醫師與品牌理念</a></div>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">購買流程</span><h2>在這裡了解，到 zh.uhealthfit.com 安全結帳</h2><p class="lead">本站專注於幫你「選對」；按下購買後會前往我們的官方商店 zh.uhealthfit.com 完成結帳。整個流程三步：</p></div>
  <div class="steps">
    <div class="step"><div class="k">1</div><h3>在本站選好產品與規格</h3><p>看系列頁、單品頁與選購指南，確定適合自己的起點與用量。</p><div class="why">不確定？做 30 秒測驗。</div></div>
    <div class="step"><div class="k">2</div><h3>前往商店安全結帳</h3><p>按「購買」會開啟 zh.uhealthfit.com 商品頁；支援 Visa、Mastercard、Apple Pay、Google Pay、PayPal、Shop Pay 等。</p><div class="why">美國眼貼滿 $79、其他商品滿 $200 免運。</div></div>
    <div class="step"><div class="k">3</div><h3>48 小時內出貨</h3><p>工作日 48 小時內處理並寄出出貨通知；30 天內未拆封可退。</p><div class="why">有問題隨時來信 service@uhealthfit.com。</div></div>
  </div>
</div></section>

<section class="sec"><div class="wrap"><div class="offer-box">
  <div class="l"><span class="eyebrow">最低門檻的開始</span><h2>先試兩個晚上，再決定要不要走下去</h2><p>護眼系列的入口，是一包兩晚份的明目冷敷眼貼體驗裝——日本製造、不含防腐劑，剛好夠你感受它適不適合自己的睡前習慣。</p>
    <div class="big">$6<small> / 兩晚體驗裝</small></div>
    <ul><li>日本製造 · 不入眼 · 不含防腐劑 · 過敏回報極少（依品牌內部客服紀錄）</li><li>喜歡再升級：1 盒 $29.99 · 3 盒一個月組 $84（推薦入門）</li><li>所有商品 30 天內未拆封可退</li></ul>
    <a class="btn btn-accent ext" data-product="eye-patches-trial" href="{shop_url(PRODUCTS['eye-patches']['trial_handle'])}">以 $6 體驗兩晚</a></div>
  <div class="r"><img src="{shop_img('files/free-trial-package.jpg?v=1758563648',700)}" alt="WiseQuest 明目冷敷眼貼兩晚體驗裝" loading="lazy"></div>
</div></div></section>
{journey(rel,'home')}
{sticky(rel)}
'''
    write('index.html', head('優健堂 UHealthFit × WiseQuest｜醫師研發草本保健 · 護眼・固齒・舒眠・順暢・肌膚・活力','由中國中西醫結合執業醫師黃醫師研發的 WiseQuest 草本保健系列：明目冷敷眼貼、草本明目膠囊、固齒膠囊、安睡膠囊、潤暢膠囊、舒緩修護霜等。美國・日本製造，成分全部公開，$6 試用裝起。',rel,'index.html','home')+nav(rel,'home')+body+footer(rel))

# ───────────────────────────── 系列頁 ─────────────────────────────
def build_series():
    for k in SERIES_ORDER:
        s=SERIES[k]; rel='../'
        cards=''.join(product_card(p,rel,wide=(len(s['products'])==1)) for p in s['products'])
        bundle=''
        if s.get('bundle'):
            b=PRODUCTS[s['bundle']]
            bundle=f'''<div class="pull" style="margin-top:24px;display:flex;flex-wrap:wrap;justify-content:space-between;gap:14px;align-items:center"><div>{esc(s['combo'][0])}：{esc(s['combo'][1])}</div><a class="btn btn-primary btn-sm" href="{rel}products/{s['bundle']}.html">看護眼三寶組合</a></div>'''
        else:
            bundle=f'''<div class="pull" style="margin-top:24px">{esc(s['combo'][0])}<small style="font-size:15px;color:var(--ink)">{esc(s['combo'][1])}</small></div>'''
        posts=''.join(post_card(p,rel) for p in POSTS if p['series']==k)
        reframe=''.join(f'<div class="card white"><div class="num">0{i+1}</div><h3>{esc(t)}</h3><p>{esc(d)}</p></div>' for i,(t,d) in enumerate(s['reframe']))
        sits=''.join(f'<li>{esc(x)}</li>' for x in s['situations'])
        others=''.join(f'<a class="scard s-{o}" href="{rel}series/{o}.html"><div class="scard-pic"><img src="{SERIES[o]["photo"]}" alt="" loading="lazy"></div><span class="series-tag"><span class="dot"></span>{SERIES[o]["en"]}</span><h3>{SERIES[o]["name"]}</h3><div class="hook">{SERIES[o]["h1"]}</div><span class="go">看系列 →</span></a>' for o in SERIES_ORDER if o!=k)
        body=f'''
{series_hero(k,rel)}
<section class="sec"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">如果你也是這樣</span><h2>這個系列為誰而做</h2></div>
  <div class="grid-2" style="align-items:start">
    <ul class="hero-trust" style="display:grid;gap:12px;margin:0;font-size:16px">{sits}</ul>
    <div class="timeline" style="margin:0"><div class="ic">⏱</div><div><b>關於時間，我們寧願第一天就說清楚：</b>多數人會先在前幾週感受到使用時的舒適感，整體狀態的穩定通常需要給自己至少 4–8 週。效果因人而異；把它當作一個生活習慣來持續。</div></div>
  </div>
</div></section>

<section class="sec bg-cream"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">我們的思路</span><h2>先理解，再選擇</h2></div>
  <div class="grid-3">{reframe}</div>
</div></section>

<section class="sec" id="products"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">{s['name']} · 產品</span><h2>怎麼選、怎麼用</h2><p class="lead">價格為美金（USD），點「購買」前往 zh.uhealthfit.com 安全結帳；點「了解」看完整成分、用法與常見問題。</p></div>
  <div class="pgrid{' pgrid-1' if len(s['products'])==1 else ''}">{cards}</div>
  {bundle}
  <p class="note" style="margin-top:18px;text-align:center">膠囊類為膳食補充劑、外用品為日常保養品，皆非藥品，不用於診斷、治療、治癒或預防任何疾病。效果因人而異。</p>
</div></section>

<section class="sec bg-green-light"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">選購指南</span><h2>關於{s['short']}，先讀這兩篇</h2></div>
  <div class="bgrid">{posts}</div>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">常見問題</span><h2>關於{s['name']}</h2></div>
  <div class="faq-list">{faq_block(s['faq'])}</div>
</div></section>
{journey(rel,'series',series_key=k)}
<section class="sec"><div class="wrap"><div class="sec-head"><span class="eyebrow">其他系列</span><h2>同一套邏輯，六個系列</h2></div><div class="grid-3">{others}</div></div></section>
{sticky(rel)}
<script type="application/ld+json">{faq_ld(s['faq'])}</script>
'''
        write(f'series/{k}.html', head(f'{s["name"]}｜{s["h1"]} · 優健堂 UHealthFit × WiseQuest', s['lead'][:150], rel, f'series/{k}.html', f'series-{k}', og_image=s['photo'])+nav(rel,'series')+body+footer(rel))

# ───────────────────────────── 單品頁 ─────────────────────────────
def build_products():
    for slug in PRODUCT_ORDER:
        p=PRODUCTS[slug]; s=SERIES[p['series']]; rel='../'
        url=buy_url(p,slug)
        variants=''
        if p.get('variants'):
            variants='<ul class="variants">'+''.join(f'<li class="{"best" if best else ""}"><span>{esc(n)}{(" <span class=tag>· "+esc(t)+"</span>") if t else ""}</span><b>{pr}</b></li>' for n,pr,t,best in p['variants'])+'</ul><p class="note">規格於 zh.uhealthfit.com 商品頁選擇；價格以結帳頁顯示為準。</p>'
        trial=''
        if p.get('trial_handle'):
            trial=f'<a class="btn btn-ghost btn-block ext" style="margin-top:8px" data-product="{slug}-trial" href="{shop_url(p["trial_handle"])}">先從 $6 兩晚體驗裝開始</a>'
        oos='<p class="note" style="margin-top:10px;color:#B84F08"><b>目前補貨中。</b>商品頁會顯示最新庫存狀態；也可以先讀選購指南，或看同系列的其他產品。</p>' if p.get('oos') else ''
        buy_label='前往護眼三寶組合頁' if p.get('is_bundle') else ('查看補貨狀態' if p.get('oos') else '前往 zh.uhealthfit.com 購買')
        cross=''.join(product_card(c,rel) for c in p['cross'])
        yes=''.join(f'<li>{esc(x)}</li>' for x in p['yes']); no=''.join(f'<li>{esc(x)}</li>' for x in p['no'])
        posts=[q for q in POSTS if q['series']==p['series']]
        pr=price_str(p, with_compare=True)
        ld=json.dumps({"@context":"https://schema.org","@type":"Product","name":p['name'],"image":p['image'],"description":p['desc'],"brand":{"@type":"Brand","name":"WiseQuest"},"url":f"{SITE_URL}/products/{slug}.html","offers":{"@type":"Offer","priceCurrency":"USD","price":str(p['price']) if p['price'] else "0","availability":"https://schema.org/OutOfStock" if p.get('oos') else "https://schema.org/InStock","url":url}},ensure_ascii=False) if not p.get('is_bundle') else ''
        body=f'''
<section class="pdp"><div class="wrap">
  <div class="gallery"><img src="{p['image']}" alt="{esc(p['name'])}" width="800" height="800" fetchpriority="high"></div>
  <div>
    <div class="crumbs"><a href="{rel}index.html">首頁</a><span>›</span><a href="{rel}series/{p['series']}.html">{s['name']}</a><span>›</span><span>{esc(p['name'])}</span></div>
    <span class="series-tag s-{p['series']}"><span class="dot"></span>{s['name']}</span>
    <h1>{esc(p['name'])}</h1><div class="en">{esc(p['en'])} · {esc(p['made'])}</div>
    <div class="hook">{esc(p['hook'])}</div>
    <p class="desc">{esc(p['long'])}</p>
    <ul class="facts"><li>{esc(p['form'])}</li><li>{esc(p['spec'])}</li><li>成分全部公開 · 第三方純度檢測</li><li>30 天內未拆封可退</li></ul>
    <div class="buybox">
      <div class="row"><div class="price">{pr}<small>{esc(p['price_note'])} · USD</small></div>{'<span class="badge badge-oos">補貨中</span>' if p.get('oos') else ('<span class="badge badge-star">單次購買 · 無訂閱</span>' if not p.get('is_bundle') else '<span class="badge badge-star">招牌組合</span>')}</div>
      {variants}
      <a class="btn btn-primary btn-block ext" data-product="{slug}" href="{url}">{buy_label}</a>
      {trial}{oos}
      <ul class="micro"><li>安全結帳</li><li>美國 {'眼貼滿 $79' if p['series']=='eye' and not p.get('is_bundle') else '滿 $200'} 免運</li><li>48 小時內出貨</li><li>30 天未拆封可退</li></ul>
      <ol class="flow"><li><b>選規格</b>在商品頁選擇數量／組合</li><li><b>安全結帳</b>Visa・Apple Pay・PayPal・Shop Pay</li><li><b>收到貨</b>工作日 48 小時內出貨</li></ol>
    </div>
  </div>
</div></section>

<section class="sec bg-cream"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">成分與用法</span><h2>你知道自己每天用的是什麼</h2></div>
  <div class="spec">
    <div class="box"><h3>成分</h3><ul><li><b>草本成分</b><span>{esc(p['herbs'])}</span></li><li><b>其他成分</b><span>{esc(p['actives'])}</span></li><li><b>製造</b><span>{esc(p['made'])}</span></li><li><b>劑型</b><span>{esc(p['form'])}</span></li></ul></div>
    <div class="box"><h3>用法與注意</h3><ul><li><b>建議用法</b><span>{esc(p['usage'])}</span></li><li><b>規格</b><span>{esc(p['spec'])}</span></li><li><b>注意事項</b><span>{esc(p['caution'])}</span></li></ul></div>
  </div>
  <div class="timeline"><div class="ic">⏱</div><div><b>誠實的期待：</b>多數人會先在前幾週感受到使用時的舒適感，整體狀態的穩定通常需要給自己至少 4–8 週。效果因人而異；若一開始沒有太多感覺，這是正常的。</div></div>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">適合誰</span><h2>這款適合你嗎？</h2></div>
  <div class="who"><div class="box yes"><h3>適合</h3><ul>{yes}</ul></div><div class="box no"><h3>不適合或請先諮詢醫師</h3><ul>{no}</ul></div></div>
</div></section>

<section class="sec bg-green-light"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">常見問題</span><h2>購買前，你可能想知道</h2></div>
  <div class="faq-list">{faq_block(p['faq'])}</div>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">搭配推薦</span><h2>常一起選的產品</h2></div>
  <div class="pgrid">{cross}</div>
</div></section>
{journey(rel,'product',product=slug)}
<div class="buybar"><div class="wrap"><div class="t"><span class="price">{pr}</span><span>{esc(p['name'])} · {esc(p['price_note'])}</span></div><a class="btn btn-primary ext" data-product="{slug}" href="{url}">{'查看組合' if p.get('is_bundle') else ('查看補貨狀態' if p.get('oos') else '前往購買')}</a></div></div>
<script type="application/ld+json">{faq_ld(p['faq'])}</script>
{('<script type="application/ld+json">'+ld+'</script>') if ld else ''}
'''
        write(f'products/{slug}.html', head(f'{p["name"]}｜{p["hook"]} · 優健堂 × WiseQuest', p['desc'], rel, f'products/{slug}.html', f'product-{slug}', og_image=p['image'])+nav(rel,'series')+body+footer(rel))

# ───────────────────────────── 部落格 ─────────────────────────────
def build_blog():
    rel='../'
    chips='<div class="chips"><button class="chip on" data-f="all">全部</button>'+''.join(f'<button class="chip" data-f="{k}">{SERIES[k]["short"]}</button>' for k in SERIES_ORDER)+'</div>'
    cards=''.join(post_card(p,rel) for p in POSTS)
    body=f'''
<section class="hero"><div class="wrap" style="grid-template-columns:1fr"><div>
  <div class="crumbs"><a href="{rel}index.html">首頁</a><span>›</span><span>選購指南</span></div>
  <span class="eyebrow">選購指南 · 12 篇</span><h1>先懂怎麼選，再決定要不要買</h1>
  <p class="lead" style="max-width:760px">我們把每個系列「市面上有哪些選項、各自負責什麼、選購時該看什麼、怎麼開始」寫成指南。每篇都誠實交代時間與不適合的人。就算最後沒有購買，也希望你更懂自己的身體、少一點焦慮。</p>
</div></div></section>
<section class="sec"><div class="wrap">{chips}<div class="bgrid">{cards}</div></div></section>
{journey(rel,'quiz')}
{sticky(rel)}
'''
    write('blog/index.html', head('選購指南｜護眼、固齒、睡眠、消化、肌膚、活力怎麼選 · 優健堂 × WiseQuest','12 篇草本保健選購指南：眼貼 vs 蒸氣眼罩、無褪黑素助眠、不含番瀉葉腸道保健、無類固醇修護霜、幫爸媽選口腔保健品……先懂怎麼選，再決定要不要買。',rel,'blog/index.html','blog')+nav(rel,'blog')+body+footer(rel))
    for p in POSTS:
        prod=PRODUCTS[p['primary_product']]; s=SERIES[p['series']]
        related=''.join(post_card(q,rel) for q in POSTS if q['slug']!=p['slug'] and q['series']==p['series'])
        more=''.join(post_card(q,rel) for q in POSTS if q['series']!=p['series'])[:0]
        ld=json.dumps({"@context":"https://schema.org","@type":"Article","headline":p['title'],"description":p['description'],"image":prod['image'],"datePublished":TODAY,"author":{"@type":"Organization","name":"優健堂 UHealthFit"},"publisher":{"@type":"Organization","name":"優健堂 UHealthFit","logo":{"@type":"ImageObject","url":LOGO}}},ensure_ascii=False)
        body=f'''
<section class="sec" style="padding-top:clamp(28px,4vw,52px)"><div class="wrap">
  <div class="article-head">
    <div class="crumbs"><a href="{rel}index.html">首頁</a><span>›</span><a href="{rel}blog/index.html">選購指南</a><span>›</span><a href="{rel}series/{p['series']}.html">{s['name']}</a></div>
    <span class="series-tag s-{p['series']}"><span class="dot"></span>{s['name']} · 選購指南</span>
    <h1>{esc(p['title'])}</h1>
    <div class="meta"><span>優健堂編輯部 · 內容依黃醫師臨床觀點與品牌產品資料整理</span><span>約 {p['reading_min']} 分鐘</span><span>更新 {TODAY}</span></div>
  </div>
  <div class="article-layout">
    <article class="article">
      {p['body']}
      <div class="disc-inline"><b>免責聲明：</b>本文為一般性資訊與選購觀點，不構成醫療建議；文中產品為膳食補充劑或日常保養品，非藥品，不用於診斷、治療、治癒或預防任何疾病。中醫相關敘述為傳統觀點的說明。效果因人而異；孕婦、哺乳期、服藥中或有健康疑慮者請先諮詢醫師。</div>
    </article>
    <aside class="aside">
      <div class="pbox"><img src="{prod['image']}" alt="{esc(prod['name'])}"><b>{esc(prod['name'])}</b><div class="price">{price_str(prod)}</div><p>{esc(prod['hook'])}</p><a class="btn btn-primary btn-sm btn-block" href="{rel}products/{p['primary_product']}.html">看產品與成分</a><a class="btn btn-ghost btn-sm btn-block ext" style="margin-top:8px" data-product="{p['primary_product']}" href="{buy_url(prod,p['primary_product'])}">前往購買</a></div>
      <div class="tbox"><h4>這篇在講什麼</h4><ul><li>市面選項各自負責什麼</li><li>選購時看的 4 件事</li><li>WiseQuest 的對應做法</li><li>誠實的期待與何時該就醫</li></ul></div>
      <div class="tbox" style="background:var(--green-light)"><h4>不只在意這一件事？</h4><p style="font-size:14px;color:var(--ink-2);margin-bottom:10px">30 秒測驗幫你排序最值得先開始的系列。</p><a class="btn btn-ghost btn-sm btn-block" href="{rel}quiz.html">開始測驗</a></div>
    </aside>
  </div>
  <div class="related"><div class="sec-head"><span class="eyebrow">延伸閱讀</span><h2>同系列的另一篇</h2></div><div class="bgrid">{related}</div></div>
</div></section>
{journey(rel,'blog',post=p)}
{sticky(rel)}
<script type="application/ld+json">{ld}</script>
'''
        write(f'blog/{p["slug"]}.html', head(f'{p["title"]} · 優健堂 × WiseQuest', p['description'], rel, f'blog/{p["slug"]}.html', f'blog-{p["slug"]}', og_image=prod['image'])+nav(rel,'blog')+body+footer(rel))

# ───────────────────────────── 測驗 ─────────────────────────────
QUIZ = [
 ('先問一個最實際的：一天裡，你有多少時間盯著螢幕？',[('8 小時以上，眼睛到下午就很乾、很累',{'eye':3}),('4–8 小時，偶爾會覺得疲勞',{'eye':2,'vitality':1}),('不多，螢幕不是我的主要困擾',{})]),
 ('晚上躺下之後，通常是什麼狀態？',[('腦子還在跑，很難放鬆',{'sleep':3}),('睡得著，但早上醒來不覺得有休息到',{'sleep':2,'vitality':1}),('大致安穩',{})]),
 ('久坐一整天、或外食應酬之後，肚子的感覺是？',[('常常頂著一股氣、不太順',{'digestive':3}),('偶爾會脹，吃清淡一點就好',{'digestive':1}),('很少有感覺',{})]),
 ('最近照鏡子，最在意的是？',[('看起來很累、暗沉、沒精神',{'vitality':3}),('換季時容易敏感、乾燥脫皮，或容易長痘',{'skin':3}),('還好，沒有特別在意',{})]),
 ('關於牙齒與牙齦——',[('我或家中長輩想為牙齦長期健康多做一點',{'dental':3}),('有在認真刷牙，暫時沒想太多',{'dental':1}),('不是我現在的重點',{})]),
 ('如果只能先開始一件事，你希望它是？',[('不用改變生活、睡前就能做的',{'eye':2,'sleep':1}),('每天隨餐一次、養成習慣就好',{'dental':1,'digestive':1,'vitality':1}),('一罐放在家裡、全家都用得到的',{'skin':2}),('先讓自己白天有精神、晚上能放鬆',{'sleep':2,'vitality':2})]),
]
def build_quiz():
    rel=''
    steps=''
    for i,(q,opts) in enumerate(QUIZ):
        btns=''.join(f'<button type="button" data-w=\'{json.dumps(w,ensure_ascii=False)}\'><span class="l">{"ABCD"[j]}</span><span>{esc(t)}</span></button>' for j,(t,w) in enumerate(opts))
        steps+=f'<div class="qstep{" on" if i==0 else ""}"><span class="eyebrow">第 {i+1} 題 / {len(QUIZ)}</span><h2>{esc(q)}</h2><div class="qopts">{btns}</div></div>'
    results=''
    for k in SERIES_ORDER:
        s=SERIES[k]; posts=[p for p in POSTS if p['series']==k]; main=PRODUCTS[s['products'][0]]
        results+=f'''<div data-r="{k}" style="display:none">
  <div class="rhead"><span class="dot" style="background:{s['color']}"></span><span class="eyebrow">你的起點</span></div>
  <h2 style="font-size:clamp(22px,3vw,30px);margin-bottom:8px">{s['name']}：{esc(s['h1'])}</h2>
  <p class="lead" style="font-size:16px">{esc(s['lead'])}</p>
  <div class="rgrid">
    <div class="rbox"><img src="{main['image']}" alt=""><h4>從這一款開始</h4><p><b>{esc(main['name'])}</b> — {esc(main['hook'])}</p><a class="btn btn-primary btn-sm" href="{rel}products/{s['products'][0]}.html">看產品</a></div>
    <div class="rbox"><h4>先讀這篇選購指南</h4><p>{esc(posts[0]['title'])}</p><p style="font-size:13px">{esc(posts[0]['excerpt'])}</p><a class="btn btn-ghost btn-sm" href="{rel}blog/{posts[0]['slug']}.html">閱讀指南</a></div>
  </div>
  <p><a href="{rel}series/{k}.html" style="color:var(--green);font-weight:700">看整個{s['name']} →</a></p>
</div>'''
    second=''.join(f'<span data-r2="{k}" style="display:none">其次是 <a href="{rel}series/{k}.html" style="color:var(--green);font-weight:700">{SERIES[k]["name"]}</a>。</span>' for k in SERIES_ORDER)
    body=f'''
<section class="hero"><div class="wrap" style="grid-template-columns:1fr"><div style="text-align:center;max-width:760px;margin:0 auto">
  <span class="eyebrow">30 秒測驗 · 6 題</span><h1>找到最值得先開始的那一件事</h1>
  <p class="lead">同時在意好幾件事很正常。這 6 題幫你排序，結果會直接對應到系列、產品與選購指南。不需註冊、結果立即顯示；僅供參考，不作為醫療診斷。</p>
</div></div></section>
<section class="sec" style="padding-top:0;margin-top:-20px"><div class="wrap"><div class="quiz-wrap"><div class="qcard" id="quiz">
  <div class="qprog"><i></i></div>
  {steps}
  <div class="qresult">
    {results}
    <p class="note" style="margin-top:6px">{second} 結果依你的回答排序，僅供參考。</p>
    <div class="email-box"><b>想把結果與對應的選購指南寄到信箱？</b>
      <form data-klaviyo-company="{KLAVIYO_COMPANY}" data-klaviyo-list="{KLAVIYO_LIST}" novalidate><input type="hidden" name="quiz_result" value=""><input type="email" name="email" placeholder="你的 Email" required aria-label="Email"><button class="btn btn-primary btn-sm" type="submit">寄給我</button></form>
      <p class="consent">送出即表示你同意收到優健堂的健康養護內容與會員優惠 Email，可隨時取消訂閱。我們不會把你的資料提供給第三方。詳見 <a class="ext" href="https://zh.uhealthfit.com/zh-hant-us/policies/privacy-policy" style="text-decoration:underline">隱私權政策</a>。</p>
      <div class="email-ok">✓ 已收到！稍後請留意信箱。</div>
    </div>
  </div>
  <div class="qnav"><button type="button" class="qback" style="visibility:hidden">← 上一題</button><span class="note">僅供參考 · 非醫療診斷</span></div>
</div></div></div></section>
{journey(rel,'quiz')}
'''
    write('quiz.html', head('30 秒測驗｜找到最值得先開始的養護系列 · 優健堂 × WiseQuest','6 題、30 秒，從護眼、固齒、睡眠、消化、肌膚、活力中找到最值得先開始的那一件事，並對應到產品與選購指南。',rel,'quiz.html','quiz')+nav(rel,'quiz')+body+footer(rel))

# ───────────────────────────── 關於 / FAQ ─────────────────────────────
def build_about():
    rel=''
    body=f'''
<section class="hero"><div class="wrap">
  <div><div class="crumbs"><a href="index.html">首頁</a><span>›</span><span>關於與黃醫師</span></div><span class="eyebrow">關於優健堂 UHealthFit × WiseQuest</span>
  <h1>值得信賴的健康之選</h1><p class="lead">優健堂 UHealthFit 是一個專注於健康與保健產品的平台，由美國紐約的 Uhealth Trading Inc. 經營。我們重視產品本身，而不是品牌大小；WiseQuest 是平台上由黃醫師研發的草本保健系列。</p></div>
  <div class="hero-visual"><img src="{IMG}/home/all-products-lineup.png" alt="優健堂全系列產品陳列"></div>
</div></section>
<section class="sec doctor bg-dark"><div class="wrap">
  <div><img src="{IMG}/home/dr-h.png" alt="黃醫師 Dr. Huang，中國中西醫結合執業醫師" loading="lazy"></div>
  <div><span class="eyebrow">研發者 · 黃醫師 Dr. Huang</span><h2>由一位看了二十年「整個人」的醫師研發</h2>
  <p>黃醫師是中國中西醫結合執業醫師，中醫全科醫師，擁有二十年臨床經驗與草本配方研發專長。她師從多位國家級名老中醫、各科教授與清末御醫傳人，學習中醫針藥特色療法；作為全科中醫師，臨床涉及內科、皮膚科、婦科、兒科，對消化系統疾病、心理睡眠疾病、神經系統疾病、呼吸系統疾病、循環系統疾病、泌尿生殖系統疾病、皮膚科常見病與痛症等均有豐富的臨床經驗，並專研中醫醫美二十年，自主研發的中藥化妝品曾獲國家發明專利。</p>
  <blockquote>「中醫講治未病，在身體逐漸衰老的過程中會發生很多衰老相關的疾病，中醫抗衰就顯得尤為重要。很多時候讓症狀暫時消失，不等於身體真的恢復。我想做的，是幫身體重新找回自己健康的狀態——用承傳千年的草本經驗，幫助身體恢復平衡。」<footer>— 黃醫師</footer></blockquote>
  <ul class="checks"><li><div>生產設施具 FDA 登記<small>核查企業與生產設施的 FDA 登記資訊（登記不等於 FDA 核准）</small></div></li><li><div>天然／有機來源成分<small>優先選擇來源清楚的草本與植物成分</small></div></li><li><div>專業經驗配方<small>以臨床觀點對應現代人的常見日常需求</small></div></li><li><div>品質安全把關<small>原料、生產、第三方純度檢測三道關卡</small></div></li><li><div>價格合理親民<small>讓長期保健更容易持續</small></div></li><li><div>只說有依據的事<small>不誇大、不神化草本、不製造焦慮</small></div></li></ul></div>
</div></section>
<section class="sec"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">品牌理念</span><h2>不壓制、不依賴，從根源支持身體</h2><p class="lead">我們相信，真正的健康，不只是沒有疾病，而是擁有一個平衡的身體、一顆安定的心，以及面對生活的力量。我們尊重現代醫學，也珍惜傳統草本智慧。</p></div>
  <div class="grid-4">
    <div class="card"><div class="num">尊重自然</div><h3>Respect Nature</h3><p>相信身體本有自我調節力；草本是支持，幫助身體恢復平衡。</p></div>
    <div class="card"><div class="num">尊重專業</div><h3>Respect Science</h3><p>尊重現代醫學證據，也珍惜傳統草本臨床經驗，開放而嚴謹。</p></div>
    <div class="card"><div class="num">關懷每一個人</div><h3>Care for People</h3><p>我們希望通過養護好物的分享，真正的幫到每個人、少一點焦慮。</p></div>
    <div class="card"><div class="num">分享知識</div><h3>Share Knowledge</h3><p>養護知識的分享，讓人理解自己的身體，如何保持平衡健康的狀態，而不是害怕或者繼續放任不管。</p></div>
  </div>
  <div class="pull">「身體一直在努力照顧你。現在，換我們照顧它。」<small>每一篇內容動筆前後，我們都問自己三個問題：它真實嗎？它對讀者真的有幫助嗎？它對得起初心嗎？</small></div>
</div></section>
<section class="sec bg-cream"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">中醫整體觀 × 現代工藝</span><h2>一套邏輯，六個系列</h2><p class="lead">中醫傳統認為身體各部位彼此牽連。每個系列的配方邏輯，都從這張「整體地圖」出發；再以現代萃取濃縮、第三方純度檢測、成分全部公開。</p></div>
  <div class="grid-3">{''.join(f'<a class="scard s-{k}" href="series/{k}.html"><span class="series-tag"><span class="dot"></span>{SERIES[k]["organ"]}</span><h3>{SERIES[k]["name"]}</h3><div class="hook">{SERIES[k]["h1"]}</div><span class="go">看系列 →</span></a>' for k in SERIES_ORDER)}</div>
</div></section>
<section class="sec"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">聯絡我們</span><h2>有問題，隨時來信</h2><p class="lead">客服信箱 <a href="mailto:service@uhealthfit.com" style="color:var(--green);font-weight:700">service@uhealthfit.com</a>。訂單、運送與退貨相關事宜，請在 zh.uhealthfit.com 商店查看政策或來信。</p></div>
  <div class="hero-cta"><a class="btn btn-primary ext" href="{SHOP}">前往 zh.uhealthfit.com 商店</a><a class="btn btn-ghost" href="faq.html">看常見問題</a></div>
</div></section>
{journey(rel,'about')}
{sticky(rel)}
'''
    write('about.html', head('關於優健堂與黃醫師｜品牌理念、品質把關 · 優健堂 UHealthFit × WiseQuest','優健堂 UHealthFit 由美國紐約 Uhealth Trading Inc. 經營；WiseQuest 草本保健系列由中國中西醫結合執業醫師黃醫師研發。尊重自然、尊重專業、關懷每一個人、分享知識。',rel,'about.html','about')+nav(rel,'about')+body+footer(rel))

FAQS = {
 '產品與使用':[('這些產品是藥嗎？可以取代我現在的治療或藥物嗎？','不是。膠囊類為膳食補充劑，乳霜、精華液與眼貼為日常保養品，都不是藥品，也不能取代醫師的診斷、治療或處方。若你正在服藥、懷孕或哺乳、或有任何健康疑慮，請在使用前先諮詢醫師或藥師。'),('多久會有感覺？','草本日常養護是累積型的。多數人會先在前幾週感受到使用時的舒適感，整體狀態的穩定通常需要給自己至少 4–8 週。效果因人而異，我們不做任何時效或結果的保證。'),('膠囊怎麼吃？需要一直吃下去嗎？','每瓶 180 粒約一個月份，建議每天兩次、每次三粒，隨餐服用（Calmoon 建議午餐後與睡前一小時）。全植物膠囊、全素。我們的設計原則是「不依賴」：狀態穩定後可以鞏固一段時間再停用。'),('可以同時用好幾個系列嗎？','可以依需要搭配（例如護眼三寶）。若同時使用多種補充劑或正在服藥，請先與醫師或藥師討論。'),('眼貼會進到眼睛裡嗎？會過敏嗎？','眼貼貼在眼周肌膚上，不入眼。日本製造、不含防腐劑，過敏回報極少（依品牌內部客服紀錄）。第一次使用前建議先做局部皮膚測試；孕婦請勿使用。')],
 '品質與製造':[('產品在哪裡製造？成分安全嗎？','明目冷敷眼貼於日本製造；膠囊、乳霜與精華液於美國依 cGMP 規範生產，生產設施具 FDA 登記（登記不等於 FDA 核准）。產品經第三方純度檢測，成分全部公開，無人工色素與防腐劑、非轉基因。'),('「FDA 登記」是什麼意思？','指我們核查相關企業與生產設施在 FDA 的登記資訊。這與「FDA 核准」不同——膳食補充劑與化妝品不經 FDA 上市前核准。'),('素食者可以吃嗎？','膠囊類皆為全植物膠囊，全素。')],
 '購買、運送與退貨':[('在這個網站可以直接結帳嗎？','本站專注於幫你「選對」。按下「購買」會前往我們的官方商店 zh.uhealthfit.com 商品頁，在那裡完成安全結帳（支援 Visa、Mastercard、Apple Pay、Google Pay、PayPal、Shop Pay 等）。'),('運費與到貨時間？','訂單於 48 小時內（工作日）處理。美國地區：眼貼滿 USD $79 免運、其他商品滿 USD $200 免運；未達門檻時運費於結帳頁顯示。眼貼與其他商品由不同倉庫出貨，可能分開送達。'),('可以退貨嗎？','收到商品後 30 天內，未拆封、封條完整並附原始包裝的商品可申請退貨；基於衛生考量，已拆封的個人護理商品無法退貨。請先來信 service@uhealthfit.com 取得退貨指引。'),('商店顯示的幣別是美金嗎？','本站所有購買連結都會帶你到 zh.uhealthfit.com 的美國市場（USD）頁面，價格與本站標示一致；若你在美國以外結帳，系統可能依配送地切換幣別，實際金額以結帳頁顯示為準。')],
 '關於平台':[('優健堂 UHealthFit 和 WiseQuest 是什麼關係？','優健堂 UHealthFit 是專注於健康與保健產品的平台，由美國紐約的 Uhealth Trading Inc. 經營；WiseQuest 是平台上由黃醫師研發的草本保健系列。'),('30 秒測驗的結果準嗎？','測驗依你的回答為六個系列排序，目的是幫你找到「先從哪裡開始」，僅供參考，不是醫療診斷。')],
}
def build_faq():
    rel=''
    groups=''.join(f'<div class="faq-group"><h3>{g}</h3>{faq_block(items)}</div>' for g,items in FAQS.items())
    allq=[q for items in FAQS.values() for q in items]
    body=f'''
<section class="hero"><div class="wrap" style="grid-template-columns:1fr"><div><div class="crumbs"><a href="index.html">首頁</a><span>›</span><span>常見問題</span></div><span class="eyebrow">常見問題</span><h1>購買前，你可能想知道</h1><p class="lead" style="max-width:720px">關於產品、品質、購買流程與平台的常見問題。找不到答案？來信 service@uhealthfit.com。</p></div></div></section>
<section class="sec"><div class="wrap"><div class="faq-list">{groups}</div></div></section>
{journey(rel,'faq')}
{sticky(rel)}
<script type="application/ld+json">{faq_ld(allq)}</script>
'''
    write('faq.html', head('常見問題｜產品、品質、購買與退貨 · 優健堂 × WiseQuest','WiseQuest 草本保健常見問題：是不是藥、多久有感、怎麼吃、在哪裡製造、如何購買與退貨。',rel,'faq.html','faq')+nav(rel,'faq')+body+footer(rel))

def build_misc():
    pages=['index.html','about.html','faq.html','quiz.html','blog/index.html']+[f'series/{k}.html' for k in SERIES_ORDER]+[f'products/{s}.html' for s in PRODUCT_ORDER]+[f'blog/{p["slug"]}.html' for p in POSTS]
    sm='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{SITE_URL}/{p}</loc><lastmod>{TODAY}</lastmod></url>\n' for p in pages)+'</urlset>\n'
    write('sitemap.xml', sm)
    write('robots.txt', f'User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n')
    shutil.copy(os.path.join(ROOT,'src','style.css'), os.path.join(DIST,'css','style.css')) if os.path.isdir(os.path.join(DIST,'css')) else (os.makedirs(os.path.join(DIST,'css')), shutil.copy(os.path.join(ROOT,'src','style.css'), os.path.join(DIST,'css','style.css')))
    os.makedirs(os.path.join(DIST,'js'),exist_ok=True); shutil.copy(os.path.join(ROOT,'src','main.js'), os.path.join(DIST,'js','main.js'))
    os.makedirs(os.path.join(DIST,'img'),exist_ok=True)
    for f in os.listdir(os.path.join(ROOT,'src','img')): shutil.copy(os.path.join(ROOT,'src','img',f), os.path.join(DIST,'img',f))
    readme=f'''# 優健堂 UHealthFit × WiseQuest 介紹網站（靜態 HTML）
製作：NTD Digital · {TODAY}

## 結構
- index.html 首頁 ｜ series/ 六大系列頁 ｜ products/ 11 個單品／組合頁 ｜ blog/ 選購指南首頁＋12 篇
- quiz.html 30 秒測驗（結果→系列／產品／指南；Email 留資送 Klaviyo Email List）｜ about.html ｜ faq.html
- css/style.css、js/main.js 共用 ｜ sitemap.xml、robots.txt

## 部署
GitHub Pages：Settings → Pages → Deploy from a branch → main / (root)。網址 https://toniachu2026.github.io/uhealthfit-zh/，綁自訂網域後改 build-src/build.py 的 SITE_URL 重建。\n\n## 怎麼改網站\n不要直接改根目錄的 HTML（34 頁會不同步）。改 `build-src/` 裡的資料與模板，然後在 repo 根目錄執行 `python3 build-src/build.py`，再 commit & push：\n- 產品、系列、FAQ、測驗題目：`build-src/build.py` 上半部的 SERIES / PRODUCTS / QUIZ / FAQS\n- 導購文章：`build-src/posts/<slug>.html`（第一行 JSON meta → `---END-META---` → HTML 片段）；新增文章請加入 build.py 的 POST_ORDER\n- 樣式／互動：`build-src/src/style.css`、`build-src/src/main.js`\n- 文案合規規範：`build-src/BRIEF.md`
- Logo 與圖片：導覽列用 uhealthfit.com 的優健堂 SVG（LOGO）、頁尾用 zh.uhealthfit.com 商店頁首的 UHealthFit 白色字標（`build-src/src/img/`）；六大系列情境照與產品實拍取自 zh.uhealthfit.com（Shopify CDN，見 build.py 的 SHOP_CDN／shop_img，`&width=` 可調尺寸），其餘產品圖取自 uhealthfit.com
上線前：
1. 綁自訂網域後，把 build-src/build.py 的 SITE_URL 改成正式網域並重建；
2. 在每頁 </head> 前插入 GTM／GA4／Meta Pixel（js/main.js 已會在購買點擊時送出 begin_checkout_redirect 與 ShopRedirect 事件、測驗完成送 quiz_complete、留資送 generate_lead）；
3. 所有「購買」按鈕都指向 zh.uhealthfit.com 商品頁並自動加上 utm_source=uhealthfit-site；
4. Klaviyo：公開 company_id Xxa5rp、List TKC3Bu（Email List, single opt-in）；留資會帶 quiz_result 屬性，可用來建 Flow。
'''
    write('README.md', readme)

if __name__=='__main__':
    build_home(); build_series(); build_products(); build_blog(); build_quiz(); build_about(); build_faq(); build_misc()
    open(os.path.join(DIST,'.nojekyll'),'w').close()  # 停用 GitHub Pages 的 Jekyll 處理
    print('built →',DIST)
