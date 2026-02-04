"""
Mock veri oluşturma scripti
Kullanım: python3 seed_data.py
"""

from app import create_app, db
from app.models import User, Category, Post, Comment, PostLike
from datetime import datetime, timedelta

def seed_database():
    app = create_app()
    
    with app.app_context():
        print("🗑️  Mevcut veritabanı temizleniyor...")
        db.drop_all()
        
        print("📦 Tablolar oluşturuluyor...")
        db.create_all()
        
        print("👥 Kullanıcılar ekleniyor...")
        # Kullanıcılar (şifre: password123)
        users = []
        user_data = [
            {'username': 'ozan', 'email': 'ozan7146@gmail.com'},
            {'username': 'Ozan', 'email': 'ozan@gmail.com'},
            {'username': 'enes', 'email': 'enes@example.com'},
            {'username': 'tuba', 'email': 'tuba@example.com'},
            {'username': 'emirhan', 'email': 'emirhan@example.com'},
        ]
        
        for data in user_data:
            user = User(username=data['username'], email=data['email'])
            user.set_password('password123')
            users.append(user)
            db.session.add(user)
        
        db.session.commit()
        print(f"   ✅ {len(users)} kullanıcı eklendi")
        
        print("📁 Kategoriler ekleniyor...")
        # Kategoriler
        category_names = ['Yazılım', 'Teknoloji', 'Gezi', 'Yaşam', 'Bilim', 
                         'Sanat', 'Spor', 'Eğitim', 'Sağlık', 'Ekonomi']
        categories = []
        
        for name in category_names:
            category = Category(name=name)
            categories.append(category)
            db.session.add(category)
        
        db.session.commit()
        print(f"   ✅ {len(categories)} kategori eklendi")
        
        print("📝 Blog yazıları ekleniyor...")
        # Blog yazıları
        posts_data = [
            {
                'title': 'Hello World! Nedir, Neden Önemlidir?',
                'content': '''Her programlama dilini öğrenmeye başladığınızda ilk yazdığınız kod "Hello World!" olur. 
                
Peki neden? Bu gelenek 1970'lerde Brian Kernighan'ın C dilini öğreten kitabında başladı. O zamandan beri tüm programcılar bu geleneği sürdürüyor.

Hello World programı aslında çok basit ama önemli bir test. Şunları kontrol eder:
- Programlama ortamınız doğru kurulmuş mu?
- Derleyici/yorumlayıcı çalışıyor mu?
- Ekrana çıktı verebiliyor musunuz?

Kısacası, Hello World bir başlangıç değil, hazır olduğunuzun kanıtıdır!''',
                'author': users[0],  # ozan
                'category': None,
                'date_posted': datetime.utcnow() - timedelta(days=5)
            },
            {
                'title': 'Junior Yazılımcıların Sık Yaptığı 5 Hata ve Çözümleri',
                'content': '''Yazılım kariyerine yeni başlayanlar genelde benzer hatalar yapar. İşte en yaygın 5 tanesi:

1. **Dokümantasyon Okumamak**: Stackoverflow'da aramadan önce resmi dokümantasyonu okuyun!

2. **Git Kullanmamak**: Her değişikliği commit edin. Gelecekteki kendiniz teşekkür edecek.

3. **Test Yazmamak**: "Kod çalışıyor, test gereksiz" demek büyük hata. Testler sizi gelecekte korur.

4. **Sürekli Copy-Paste**: Kodu anlamadan kopyalamak sizi geliştirmez. Satır satır okuyun.

5. **Yardım İstemekten Çekinmek**: Takılırsanız sorun! Senior'lar yardım etmek ister.

Unutmayın, herkes bu hataları yapar. Önemli olan onlardan ders çıkarmak!''',
                'author': users[2],  # enes
                'category': categories[0],  # Yazılım
                'date_posted': datetime.utcnow() - timedelta(days=4)
            },
            {
                'title': 'Ertelemeyi Bırakın: 2 Dakika Kuralı Nedir?',
                'content': '''Erteleme herkesin başına gelir. Ama 2 Dakika Kuralı bunu çözebilir!

**Kural çok basit:** Bir iş 2 dakikadan az sürüyorsa, hemen yapın!

Örnekler:
- Bulaşık yıkamak
- E-mail cevaplamak  
- Yatağı toplamak
- Dosya düzenlemek

Neden işe yarıyor?
1. Küçük işler birikmez
2. Yapılacaklar listesi kısalır
3. Momentum kazanırsınız
4. Zihinsel yük azalır

Büyük işler için de çalışır: "2 dakika başla" deyin kendinize. Genelde devam edersiniz!

Deneyin, hayatınız değişecek! 🚀''',
                'author': users[2],  # enes
                'category': categories[3],  # Yaşam
                'date_posted': datetime.utcnow() - timedelta(days=3)
            },
            {
                'title': 'Dijital Göçebe (Digital Nomad) Olmak İsteyenler İçin 5 İpucu',
                'content': '''Laptopunuzla dünyanın her yerinden çalışmak hayal değil! İşte başlamanız için 5 ipucu:

1. **İyi İnternet Şart**: Her yere gitmeden önce internet hızını araştırın. Coworking space'ler güvenli seçenek.

2. **Sağlık Sigortası**: Seyahat sigortası alın. Digital nomad'lar için özel paketler var.

3. **Zaman Dilimi**: Müşterilerinizle overlapping saatler olsun. Çok farklı zaman dilimlerinde çalışmak yorucu.

4. **Bütçe Planlama**: Her şehir farklı. Bali ucuz, Tokyo pahalı. Gelir-gider dengenizi kurun.

5. **Topluluk**: Yalnız kalmayin. Nomad gruplarına katılın, meetup'lara gidin.

En popüler şehirler: Bali, Chiang Mai, Medellín, Lizbon, Tiflis.

Başlamak için mükemmel zaman yok. Sadece başlayın! ✈️''',
                'author': users[3],  # tuba
                'category': categories[2],  # Gezi
                'date_posted': datetime.utcnow() - timedelta(days=2)
            },
            {
                'title': 'Sabahları Yorgun Uyanmaya Son: Uyku Kalitenizi Artırın',
                'content': '''8 saat uyuyorsunuz ama yine yorgunsunuz? Sorun süre değil, kalite!

**Uyku Kalitenizi Artırma Yöntemleri:**

🌙 **Uyku Ortamı**
- Oda sıcaklığı 18-20°C olsun
- Karanlık perdeleri kullanın
- Mavi ışık filtresi kullanın

⏰ **Düzenli Uyku Saatleri**
- Her gün aynı saatte yatın
- Hafta sonları da düzeni bozmayın
- 7-9 saat uyuyun

📵 **Ekranlardan Uzak Durun**
- Yatmadan 1 saat önce telefonu bırakın
- Blue light filtresini açın
- Kitap okumayı deneyin

☕ **Kafein Kontrolü**
- Öğleden sonra kafein almayın
- Alkol uyku kalitesini düşürür

Bunları deneyin, 2 hafta sonra farkı göreceksiniz! 😴''',
                'author': users[3],  # tuba
                'category': categories[8],  # Sağlık
                'date_posted': datetime.utcnow() - timedelta(days=1)
            },
            {
                'title': 'Para Biriktirmeye Başlamak İçin 3 Basit Adım (Bütçe Planı)',
                'content': '''Para biriktirmek zor görünüyor ama küçük adımlarla başlayabilirsiniz!

**1. 50/30/20 Kuralı**
- %50 → İhtiyaçlar (kira, faturalar, yemek)
- %30 → İstekler (eğlence, hobiler)
- %20 → Birikim

**2. Otomatik Birikim**
Maaş gelir gelmez %10'unu başka hesaba aktarın. Görmezseniz harcamazsınız!

**3. Gereksiz Abonelikleri İptal Edin**
Netflix, Spotify, gym... Kullanmadığınız her şeyi iptal edin. Ayda 500₺+ tasarruf!

**Bonus İpucu:** "Küçük harcamalar" önemli değil demeyin. Günde 50₺ kahve = Ayda 1500₺!

Başarının sırrı: Küçük başlayın, disiplinli olun. İlk 10,000₺'yi biriktirmek en zor, sonrası kolay! 💰''',
                'author': users[3],  # tuba
                'category': categories[9],  # Ekonomi
                'date_posted': datetime.utcnow() - timedelta(hours=12)
            },
            {
                'title': "Antarktika'nın Sisifos'u: Bir Penguen Neden Yürür?",
                'content': '''Antarktika'da bir belgesel ekibi garip bir şey fark etti: Bir penguen koloniden ayrılıp tek başına içeriye doğru yürümeye başladı.

Nereye gidiyordu? Denize mi? Hayır. Yiyeceğe mi? Hayır. Koloniye mi? Hayır.

İçeride 70km boyunca hiçbir şey yok. Sadece buz ve ölüm.

Araştırmacılar müdahale etmek istedi ama yasak. Doğaya karışamazsınız. Penguen yürümeye devam etti.

**Neden?**

Bilim hala cevabı bilmiyor. Bazı teoriler:
- Stres veya travma
- Hastalık
- Yönünü şaşırmış olabilir
- Belki de... bir amaç arıyordu?

Bu penguen bize bir şey hatırlatıyor: Bazen anlamsız gibi görünen yolculuklar, yolculuğun ta kendisi için yapılır.

Ya da belki penguen sadece "Ben burada değilim" demiştir. Kim bilebilir? 🐧''',
                'author': users[4],  # emirhan
                'category': categories[3],  # Yaşam
                'date_posted': datetime.utcnow() - timedelta(hours=6)
            },
            {
                'title': 'Uzaylılar varsa neden hala karşılaşmadık?',
                'content': '''Bu soruya "Fermi Paradoksu" denir. Mantık çok basit:

1. Evren 13.8 milyar yaşında
2. 100-400 milyar galaksi var
3. Her galakside milyarlarca gezegen var
4. İhtimal olarak binlerce uygarlık olmalı

**Peki nerede onlar?**

En popüler teoriler:

🌍 **Great Filter Teorisi**
Belki akıllı yaşam çok nadir çünkü bir "filtre" var. Ya biz filtreyi geçtik (şanslıyız!) ya da henüz gelecek (korkutucu).

📡 **İletişim Sorunu**
Belki onlar farklı dalga boylarında iletişim kuruyor. Biz radyo sinyali ararken onlar kuantum mesajlaşma kullanıyor olabilir.

🤫 **Zoo Hipotezi**
Belki bizi görüyorlar ama müdahale etmiyorlar. Prime Directive gibi. Gözlem altındayız!

⏰ **Zaman Problemi**
Belki uygarlıklar kısa ömürlü. Kendini yok etmeden önce sadece birkaç bin yıl var. Evrende overlap olmuyoruz.

Hangisi gerçek? Bilemiyoruz. Ama cevap keşfetmek için sabırsızlanıyoruz! 👽''',
                'author': users[4],  # emirhan
                'category': categories[4],  # Bilim
                'date_posted': datetime.utcnow() - timedelta(hours=2)
            },
        ]
        
        posts = []
        for post_data in posts_data:
            post = Post(
                title=post_data['title'],
                content=post_data['content'],
                author=post_data['author'],
                category=post_data['category'],
                date_posted=post_data['date_posted']
            )
            posts.append(post)
            db.session.add(post)
        
        db.session.commit()
        print(f"   ✅ {len(posts)} blog yazısı eklendi")
        
        print("❤️  Beğeniler ekleniyor...")
        # Beğeniler
        likes_data = [
            {'user': users[3], 'post': posts[1]},  # tuba -> Junior Yazılımcıların...
            {'user': users[4], 'post': posts[4]},  # emirhan -> Sabahları Yorgun...
            {'user': users[4], 'post': posts[2]},  # emirhan -> Ertelemeyi Bırakın...
        ]
        
        for like_data in likes_data:
            like = PostLike(user=like_data['user'], post=like_data['post'])
            db.session.add(like)
        
        db.session.commit()
        print(f"   ✅ {len(likes_data)} beğeni eklendi")
        
        print("💬 Yorumlar ekleniyor...")
        # Yorumlar
        comments_data = [
            {
                'body': 'bayıldımmm, çok teşekkürlerr',
                'author': users[3],  # tuba
                'post': posts[1],  # Junior Yazılımcıların...
                'date_posted': datetime.utcnow() - timedelta(hours=3)
            }
        ]
        
        for comment_data in comments_data:
            comment = Comment(
                body=comment_data['body'],
                author=comment_data['author'],
                post=comment_data['post'],
                date_posted=comment_data['date_posted']
            )
            db.session.add(comment)
        
        db.session.commit()
        print(f"   ✅ {len(comments_data)} yorum eklendi")
        
        print("\n✨ Veritabanı başarıyla oluşturuldu!")
        print("\n📊 Özet:")
        print(f"   👥 Kullanıcılar: {len(users)}")
        print(f"   📁 Kategoriler: {len(categories)}")
        print(f"   📝 Blog Yazıları: {len(posts)}")
        print(f"   ❤️  Beğeniler: {len(likes_data)}")
        print(f"   💬 Yorumlar: {len(comments_data)}")
        print("\n🔑 Tüm kullanıcılar için şifre: password123")

if __name__ == '__main__':
    seed_database()
