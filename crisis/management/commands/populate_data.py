from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db.models import Sum
from crisis.models import CrisisPost, PostSection
from volunteers.models import VolunteerApplication
from donations.models import DonationMoney, DonationGoods
from updates.models import CrisisUpdate, Comment
from decimal import Decimal
import random
from allauth.account.models import EmailAddress

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate database with sample data for CrisisAID'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('🚀 Starting data population...'))
        
        # Clear existing data (optional)
        self.stdout.write('🗑️  Clearing existing data...')
        Comment.objects.all().delete()
        CrisisUpdate.objects.all().delete()
        DonationGoods.objects.all().delete()
        DonationMoney.objects.all().delete()
        VolunteerApplication.objects.all().delete()
        PostSection.objects.all().delete()
        CrisisPost.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()
        
        # Create users
        self.stdout.write('👥 Creating users...')
        users = self.create_users()
        
        # Create crisis posts
        self.stdout.write('🚨 Creating crisis posts...')
        crisis_posts = self.create_crisis_posts(users)
        
        # Create post sections
        self.stdout.write('📋 Creating post sections...')
        self.create_post_sections(crisis_posts, users)
        
        # Create volunteer applications
        self.stdout.write('🙋 Creating volunteer applications...')
        volunteer_apps = self.create_volunteer_applications(users, crisis_posts)
        
        # Create donations
        self.stdout.write('💰 Creating donations...')
        self.create_donations(users, crisis_posts)
        
        # Create updates
        self.stdout.write('📰 Creating crisis updates...')
        updates = self.create_updates(users, crisis_posts, volunteer_apps)
        
        # Create comments
        self.stdout.write('💬 Creating comments...')
        self.create_comments(users, updates)
        
        self.stdout.write(self.style.SUCCESS('\n✅ Data population completed successfully!'))
        self.print_summary()

    def create_users(self):
        """Create test users with verified emails"""
        users_data = [
            {'username': 'rahim_ahmed', 'email': 'rahim@example.com', 'password': 'password123', 'first_name': 'Rahim', 'last_name': 'Ahmed'},
            {'username': 'karim_khan', 'email': 'karim@example.com', 'password': 'password123', 'first_name': 'Karim', 'last_name': 'Khan'},
            {'username': 'fatima_begum', 'email': 'fatima@example.com', 'password': 'password123', 'first_name': 'Fatima', 'last_name': 'Begum'},
            {'username': 'salma_khatun', 'email': 'salma@example.com', 'password': 'password123', 'first_name': 'Salma', 'last_name': 'Khatun'},
            {'username': 'jamil_hossain', 'email': 'jamil@example.com', 'password': 'password123', 'first_name': 'Jamil', 'last_name': 'Hossain'},
            {'username': 'nasrin_akter', 'email': 'nasrin@example.com', 'password': 'password123', 'first_name': 'Nasrin', 'last_name': 'Akter'},
            {'username': 'habib_rahman', 'email': 'habib@example.com', 'password': 'password123', 'first_name': 'Habib', 'last_name': 'Rahman'},
            {'username': 'ayesha_islam', 'email': 'ayesha@example.com', 'password': 'password123', 'first_name': 'Ayesha', 'last_name': 'Islam'},
            {'username': 'rafiq_uddin', 'email': 'rafiq@example.com', 'password': 'password123', 'first_name': 'Rafiq', 'last_name': 'Uddin'},
            {'username': 'taslima_jahan', 'email': 'taslima@example.com', 'password': 'password123', 'first_name': 'Taslima', 'last_name': 'Jahan'},
        ]
        
        users = []
        for user_data in users_data:
            user = User.objects.create_user(**user_data)
            users.append(user)
            
            # NEW: Create and verify email address
            EmailAddress.objects.create(
                user=user,
                email=user.email,
                verified=True,  # Mark as verified
                primary=True
            )
            
            self.stdout.write(f'  ✓ Created user: {user.username} (email verified)')
        
        return users

    def create_crisis_posts(self, users):
        """Create crisis posts"""
        crisis_data = [
            {
                'title': 'সিলেটে ভয়াবহ বন্যা - Severe Flooding in Sylhet',
                'description': 'Unprecedented floods have affected over 5 million people in Sylhet division. Immediate relief needed for displaced families. Water levels rising rapidly, many areas completely submerged. Urgent need for food, clean water, and medical supplies. সিলেটে অভূতপূর্ব বন্যায় ৫০ লাখেরও বেশি মানুষ ক্ষতিগ্রস্ত।',
                'post_type': 'national',
                'location': 'Sylhet Division, Bangladesh',
                'status': 'approved',
                'owner': users[0]
            },
            {
                'title': 'Cyclone Mocha Aftermath - Coastal Areas',
                'description': 'Cyclone Mocha has devastated coastal regions. Thousands of homes destroyed in Cox\'s Bazar, Chattogram, and surrounding areas. Need emergency shelter, food, and medical assistance. Infrastructure badly damaged. Fishing communities severely affected.',
                'post_type': 'national',
                'location': 'Coastal Bangladesh',
                'status': 'approved',
                'owner': users[1]
            },
            {
                'title': 'ঢাকার মিরপুরে অগ্নিকাণ্ড - Fire Emergency in Mirpur',
                'description': 'Major fire in Mirpur residential area. 200+ families affected. Immediate need for temporary shelter, clothing, and food supplies. Many lost their homes and belongings overnight. মিরপুরে বড় অগ্নিকাণ্ডে ২০০+ পরিবার ক্ষতিগ্রস্ত।',
                'post_type': 'district',
                'location': 'Mirpur, Dhaka',
                'status': 'approved',
                'owner': users[2]
            },
            {
                'title': 'পাহাড়ি ঢল - Chittagong Hill Tracts Landslide',
                'description': 'Heavy rainfall triggered landslides in Rangamati and Bandarban. Multiple villages cut off. Need rescue operations, medical teams, and relief supplies. Roads blocked, communication lines down.',
                'post_type': 'district',
                'location': 'Chittagong Hill Tracts',
                'status': 'approved',
                'owner': users[3]
            },
            {
                'title': 'গৃহহীন পরিবার - Family Home Destroyed by Fire',
                'description': 'Our house in Uttara caught fire last night due to electrical short circuit. We lost everything. Family of 6 including 3 children. Need immediate help with shelter, food, and basic necessities. আমরা গৃহহীন হয়ে পড়েছি।',
                'post_type': 'individual',
                'location': 'Uttara, Dhaka',
                'status': 'approved',
                'owner': users[4]
            },
            {
                'title': 'ক্যান্সার চিকিৎসা সহায়তা - Cancer Treatment Help',
                'description': 'My mother needs urgent cancer treatment at BSMMU. We have exhausted all savings. Looking for financial help for chemotherapy and medication. Treatment cost: 5 Lakh BDT. আমার মায়ের জরুরি ক্যান্সার চিকিৎসা দরকার।',
                'post_type': 'individual',
                'location': 'Khulna',
                'status': 'approved',
                'owner': users[5]
            },
            {
                'title': 'Earthquake Relief - Rangpur Division',
                'description': 'Recent earthquake (magnitude 5.2) caused significant damage in northern region. Multiple buildings collapsed in Rangpur city. Rescue operations ongoing. Many families living in makeshift tents.',
                'post_type': 'national',
                'location': 'Rangpur Division',
                'status': 'pending',
                'owner': users[6]
            },
            {
                'title': 'স্কুল মেরামত - School Building Repair Needed',
                'description': 'Local primary school roof collapsed during Kalbaishakhi storm in Barisal. 500 students affected. Classes suspended. Need funds to rebuild. Estimated cost: 10 Lakh BDT.',
                'post_type': 'individual',
                'location': 'Barisal',
                'status': 'pending',
                'owner': users[7]
            },
            {
                'title': 'রোহিঙ্গা ক্যাম্পে অগ্নিকাণ্ড - Rohingya Camp Fire Emergency',
                'description': 'Massive fire in Kutupalong refugee camp, Cox\'s Bazar. Thousands displaced. Urgent need for shelter materials, food, water, and medical supplies. International assistance required.',
                'post_type': 'district',
                'location': "Cox's Bazar",
                'status': 'approved',
                'owner': users[0]
            },
            {
                'title': 'খরা - Drought Crisis in Rajshahi',
                'description': 'Severe drought affecting Barind region farming communities. Crops failing due to lack of water. Farmers need financial support and irrigation water supply. Food security at risk.',
                'post_type': 'district',
                'location': 'Rajshahi',
                'status': 'approved',
                'owner': users[1]
            },
            {
                'title': 'নদী ভাঙন - River Erosion in Char Areas',
                'description': 'Jamuna river erosion displacing hundreds of families in Sirajganj. Homes, agricultural land being washed away. Need immediate relocation assistance and shelter.',
                'post_type': 'district',
                'location': 'Sirajganj',
                'status': 'approved',
                'owner': users[8]
            },
            {
                'title': 'শীতার্ত মানুষের সেবা - Winter Relief for Homeless',
                'description': 'Extreme cold wave affecting northern districts. Homeless people and poor families need warm clothes and blankets urgently. Target: 5000 families.',
                'post_type': 'district',
                'location': 'Dinajpur, Panchagarh',
                'status': 'approved',
                'owner': users[9]
            },
        ]
        
        crisis_posts = []
        for data in crisis_data:
            post = CrisisPost.objects.create(**data)
            crisis_posts.append(post)
            self.stdout.write(f'  ✓ Created crisis: {post.title[:50]}...')
        
        return crisis_posts

    def create_post_sections(self, crisis_posts, users):
        """Create sections for crisis posts"""
        section_templates = {
            'shelter': [
                'Temporary shelters set up at Govt. Primary School. Capacity: 500 people. 24/7 security available.',
                'Community center converted to emergency shelter. Food and medical facilities available.',
                'Relief camps established in 5 locations across the affected area.',
                'শরণার্থী শিবির স্থাপন করা হয়েছে স্থানীয় স্কুলে। ধারণক্ষমতা: ৫০০ জন।',
            ],
            'resources': [
                'Need: Rice (5000kg), Lentils (2000kg), Cooking oil (500L), Water bottles (10000), চাল, ডাল, তেল প্রয়োজন',
                'Required: Blankets (1000), Warm clothes, Baby food, Sanitary supplies, Mosquito nets',
                'Urgent: Medicines, First aid kits, ORS packets, Water purification tablets',
                'দরকার: কম্বল (১০০০), শিশু খাবার, স্যানিটারি সামগ্রী, ওষুধপত্র',
            ],
            'fund': [
                'Target: 50,00,000 BDT. Collected: 12,50,000 BDT (25%) | লক্ষ্যমাত্রা: ৫০ লক্ষ টাকা',
                'Goal: 20,00,000 BDT for medical supplies and food distribution',
                'Funds needed: 15,00,000 BDT for rebuilding homes and infrastructure',
            ],
            'hotline': [
                '📞 Emergency Hotline: +880-1712-345678\n📞 Medical Emergency: +880-1798-765432\n📞 Volunteer Coordination: +880-1555-123456\n📞 খাদ্য বিতরণ: +880-1666-777888',
                '📞 Relief Center: +880-1666-777888\n📞 Food Distribution: +880-1444-555666\n📞 সাহায্য হটলাইন: +880-1999-888777',
            ],
            'distribution': [
                'Food Distribution Points:\n1. Upazila Parishad - 9 AM to 5 PM\n2. Community Center - 10 AM to 4 PM\n3. Local School Ground - 8 AM to 6 PM',
                'Distribution Schedule: Morning 8-11 AM, Evening 4-7 PM. Bring ID proof for verification.',
            ],
            'updates': [
                'Latest: Relief materials distributed to 500 families today. Medical team treating patients.',
                'Update: Water purification units installed in 5 locations. Clean water now available.',
                'Progress: 100 temporary shelters completed. Food packets distributed daily.',
            ],
        }
        
        # Add sections to approved posts
        approved_posts = [p for p in crisis_posts if p.status == 'approved']
        for post in approved_posts:
            num_sections = random.randint(3, 5)
            section_types = random.sample(list(section_templates.keys()), num_sections)
            
            for section_type in section_types:
                content = random.choice(section_templates[section_type])
                PostSection.objects.create(
                    post=post,
                    section_type=section_type,
                    content=content,
                    created_by=random.choice(users)
                )

    def create_volunteer_applications(self, users, crisis_posts):
        """Create volunteer applications"""
        messages = [
            "I have 5 years of experience in disaster relief with BRAC. I'm ready to help immediately.",
            "I'm a medical professional (MBBS) and want to volunteer in the affected area.",
            "I have access to a truck and can help with transportation of relief supplies.",
            "I'm a local resident and know the area well. Can assist with coordination.",
            "I want to help with food distribution and shelter management. Available full-time.",
            "I have experience in first aid and emergency response. Red Crescent trained volunteer.",
            "আমি দুর্যোগ ব্যবস্থাপনায় অভিজ্ঞ। সাহায্য করতে প্রস্তুত।",
            "I'm a teacher and can help with children's education and psychological support.",
        ]
        
        applications = []
        approved_posts = [p for p in crisis_posts if p.status == 'approved']
        
        for post in approved_posts:
            num_volunteers = random.randint(3, 7)
            volunteers = random.sample(users, min(num_volunteers, len(users)))
            
            for i, volunteer in enumerate(volunteers):
                status = 'approved' if i < 2 else random.choice(['approved', 'pending', 'rejected'])
                app = VolunteerApplication.objects.create(
                    user=volunteer,
                    crisis_post=post,
                    message=random.choice(messages),
                    status=status
                )
                applications.append(app)
                self.stdout.write(f'  ✓ {volunteer.username} applied for: {post.title[:30]}... [{status}]')
        
        return applications

    def create_donations(self, users, crisis_posts):
        """Create donations"""
        approved_posts = [p for p in crisis_posts if p.status == 'approved']
        
        # Money donations with realistic Bangladeshi amounts
        amounts = [500, 1000, 2000, 3000, 5000, 10000, 15000, 20000, 25000, 50000, 100000]
        payment_methods = ['bkash', 'nagad', 'rocket', 'bank', 'card']
        
        for post in approved_posts:
            num_donations = random.randint(8, 15)
            
            for _ in range(num_donations):
                # Mix of logged-in and anonymous donations
                if random.choice([True, False, False]):  # 33% logged in
                    donor = random.choice(users)
                    DonationMoney.objects.create(
                        crisis_post=post,
                        donor=donor,
                        amount=Decimal(random.choice(amounts)),
                        payment_method=random.choice(payment_methods),
                        transaction_id=f'TXN{random.randint(100000, 999999)}',
                        message=random.choice([
                            'Stay strong! আল্লাহ সাহায্য করুন',
                            'Hope this helps',
                            'Praying for you all',
                            'সাহায্য করতে পেরে খুশি',
                            '',
                            'May Allah help everyone'
                        ]),
                        is_anonymous=random.choice([True, False])
                    )
                else:
                    # Anonymous donation
                    DonationMoney.objects.create(
                        crisis_post=post,
                        donor_name=random.choice([
                            'Anonymous Donor',
                            'A Well-wisher',
                            'Concerned Citizen',
                            'শুভাকাঙ্ক্ষী',
                            'Local Business',
                            'Community Member'
                        ]),
                        donor_email=f'donor{random.randint(1, 200)}@example.com',
                        donor_phone=f'017{random.randint(10000000, 99999999)}',
                        amount=Decimal(random.choice(amounts)),
                        payment_method=random.choice(payment_methods),
                        transaction_id=f'TXN{random.randint(100000, 999999)}',
                        message='',
                        is_anonymous=True
                    )
        
        # Goods donations
        goods_items = [
            '50 blankets, 30 mattresses, 100 bottles water | ৫০টি কম্বল, ৩০টি তোষক',
            '20kg rice, 10kg lentils, 5L cooking oil | ২০ কেজি চাল, ১০ কেজি ডাল',
            '100 hygiene kits, 50 mosquito nets | ১০০টি পরিচ্ছন্নতা কিট',
            'Medicines worth 50,000 BDT, First aid supplies | ওষুধপত্র',
            '200 pieces of clothing, 50 pairs of shoes | ২০০টি কাপড়, ৫০ জোড়া জুতা',
            '10 tents, 20 tarpaulins, 100 plastic sheets | ১০টি তাঁবু, ২০টি ত্রিপল',
            'Baby food, diapers, milk powder for 50 infants',
            'Water purification tablets, ORS packets (5000), sanitary pads',
        ]
        
        for post in approved_posts:
            num_goods = random.randint(5, 10)
            
            for _ in range(num_goods):
                if random.choice([True, False]):
                    donor = random.choice(users)
                    DonationGoods.objects.create(
                        crisis_post=post,
                        donor=donor,
                        item_description=random.choice(goods_items),
                        quantity=f'{random.randint(20, 200)} items',
                        delivery_method=random.choice(['Self-delivery', 'Courier', 'Pickup arranged', 'সরাসরি পৌঁছে দেওয়া হবে']),
                        message=random.choice(['', 'Hope this helps', 'Will deliver tomorrow', 'আগামীকাল পৌঁছানো হবে']),
                        is_anonymous=random.choice([True, False])
                    )
                else:
                    DonationGoods.objects.create(
                        crisis_post=post,
                        donor_name=random.choice([
                            'Local Business Association',
                            'Community Group',
                            'Dhaka Rotary Club',
                            'স্থানীয় ব্যবসায়ী সমিতি',
                            'Youth Organization',
                            'Mosque Committee'
                        ]),
                        donor_email=f'org{random.randint(1, 100)}@example.com',
                        donor_phone=f'018{random.randint(10000000, 99999999)}',
                        item_description=random.choice(goods_items),
                        quantity=f'{random.randint(100, 1000)} items',
                        delivery_method='Arranged pickup | পিকআপের ব্যবস্থা করা হয়েছে',
                        is_anonymous=False
                    )
        
        self.stdout.write(f'  ✓ Created donations for all approved posts')

    def create_updates(self, users, crisis_posts, volunteer_apps):
        """Create crisis updates"""
        update_templates = [
            {
                'title': 'Relief Distribution - Day 1 | ত্রাণ বিতরণ - দিন ১',
                'description': 'Successfully distributed food packets to 500 families today. Medical team from DMC has arrived and set up a temporary clinic. Water purification units are now operational. আজ ৫০০ পরিবারে খাদ্য বিতরণ সম্পন্ন হয়েছে।'
            },
            {
                'title': 'Shelter Construction Progress | আশ্রয়কেন্দ্র নির্মাণ',
                'description': 'Completed construction of 50 temporary shelters using tarpaulins and bamboo. Another 100 under construction. Local volunteers and Army personnel working together. ৫০টি অস্থায়ী আশ্রয়কেন্দ্র নির্মাণ সম্পন্ন।'
            },
            {
                'title': 'Medical Camp Update | চিকিৎসা শিবির',
                'description': 'Treated 300+ patients today. Most common issues: waterborne diseases, dehydration, minor injuries, and infections. Doctors from Dhaka Medical College assisting. Need more antibiotics and IV fluids. আজ ৩০০+ রোগীর চিকিৎসা সম্পন্ন।'
            },
            {
                'title': 'Donation Update - Thank You! | দাতাদের ধন্যবাদ',
                'description': 'Overwhelmed by the support from all over Bangladesh! Received 2 tons of rice, 1000 blankets, 500kg lentils, medicines, and numerous other supplies from various donors. Distribution begins tomorrow morning at 8 AM.'
            },
            {
                'title': 'Rescue Operations Completed | উদ্ধার কার্যক্রম সম্পন্ন',
                'description': 'All stranded families from remote char areas have been rescued and moved to safe locations. Fire Service, Navy, and local volunteers did amazing work. Focus now shifts to relief and rehabilitation.'
            },
            {
                'title': 'Infrastructure Assessment | অবকাঠামো মূল্যায়ন',
                'description': 'Surveyed the damage: 200 homes completely destroyed, 500 partially damaged. 3 schools and 1 health center need repairs. Road access restored to main areas. Electricity still not available in remote zones.'
            },
            {
                'title': 'Clean Water Supply | বিশুদ্ধ পানি সরবরাহ',
                'description': 'Installed 10 deep tube wells and 5 water purification units. Now serving 2000 families with clean drinking water. WASA engineers helping with water quality testing.'
            },
            {
                'title': 'Children Education Program | শিশু শিক্ষা কর্মসূচি',
                'description': 'Started temporary schooling for 200 children in the relief camp. Teachers volunteering their time. Need notebooks, pencils, and educational materials.'
            },
        ]
        
        updates = []
        approved_posts = [p for p in crisis_posts if p.status == 'approved']
        approved_volunteers = [a for a in volunteer_apps if a.status == 'approved']
        
        for post in approved_posts:
            num_updates = random.randint(3, 6)
            
            # Get volunteers for this post
            post_volunteers = [v for v in approved_volunteers if v.crisis_post == post]
            
            for i in range(num_updates):
                update_data = random.choice(update_templates)
                
                # Creator can be post owner or approved volunteer
                if post_volunteers and random.choice([True, False]):
                    creator = random.choice(post_volunteers).user
                else:
                    creator = post.owner
                
                update = CrisisUpdate.objects.create(
                    crisis_post=post,
                    created_by=creator,
                    title=update_data['title'],
                    description=update_data['description']
                )
                updates.append(update)
                self.stdout.write(f'  ✓ Update created for: {post.title[:30]}...')
        
        return updates

    def create_comments(self, users, updates):
        """Create comments on updates"""
        comment_texts = [
            'Great work! Keep it up! অসাধারণ কাজ!',
            'Thank you for the update. Praying for everyone affected. সবার জন্য দোয়া রইল।',
            'How can I help? I want to volunteer. আমি কীভাবে সাহায্য করতে পারি?',
            'This is amazing progress! চমৎকার অগ্রগতি!',
            'Stay safe everyone. Allah bless you all. আল্লাহ সবাইকে হেফাজত করুন।',
            'Donated 10,000 BDT. Hope it helps! ১০,০০০ টাকা দান করলাম।',
            'Shared this with my network. More help is coming.',
            'Is there a specific list of items needed? কী কী জিনিস দরকার?',
            'Can we visit the relief camp? আমরা কি ক্যাম্পে যেতে পারি?',
            'Incredible effort by all volunteers! স্বেচ্ছাসেবকদের প্রশংসনীয় কাজ!',
            'May Allah reward you all. আল্লাহ সবাইকে উত্তম প্রতিদান দিন।',
            'Need more information about food distribution schedule.',
        ]
        
        for update in updates:
            num_comments = random.randint(3, 10)
            commenters = random.sample(users, min(num_comments, len(users)))
            
            for commenter in commenters:
                Comment.objects.create(
                    update=update,
                    user=commenter,
                    text=random.choice(comment_texts)
                )

    def print_summary(self):
        """Print summary of created data"""
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('📊 DATA SUMMARY'))
        self.stdout.write('='*60)
        self.stdout.write(f'👥 Users: {User.objects.filter(is_superuser=False).count()}')
        self.stdout.write(f'🚨 Crisis Posts: {CrisisPost.objects.count()}')
        self.stdout.write(f'   - Approved: {CrisisPost.objects.filter(status="approved").count()}')
        self.stdout.write(f'   - Pending: {CrisisPost.objects.filter(status="pending").count()}')
        self.stdout.write(f'📋 Post Sections: {PostSection.objects.count()}')
        self.stdout.write(f'🙋 Volunteer Applications: {VolunteerApplication.objects.count()}')
        self.stdout.write(f'   - Approved: {VolunteerApplication.objects.filter(status="approved").count()}')
        self.stdout.write(f'   - Pending: {VolunteerApplication.objects.filter(status="pending").count()}')
        self.stdout.write(f'💰 Money Donations: {DonationMoney.objects.count()}')
        
        # Fixed: Using Sum correctly
        total_amount = DonationMoney.objects.aggregate(total=Sum('amount'))['total'] or 0
        self.stdout.write(f'   - Total Amount: {total_amount:,.2f} BDT')
        
        self.stdout.write(f'📦 Goods Donations: {DonationGoods.objects.count()}')
        self.stdout.write(f'📰 Crisis Updates: {CrisisUpdate.objects.count()}')
        self.stdout.write(f'💬 Comments: {Comment.objects.count()}')
        self.stdout.write('='*60)
        self.stdout.write(self.style.SUCCESS('\n✅ All test data created successfully!'))
        self.stdout.write('\n📝 Test User Credentials (All passwords: password123):')
        self.stdout.write('   Username: rahim_ahmed   | Password: password123')
        self.stdout.write('   Username: karim_khan    | Password: password123')
        self.stdout.write('   Username: fatima_begum  | Password: password123')
        self.stdout.write('   Username: salma_khatun  | Password: password123')
        self.stdout.write('   Username: jamil_hossain | Password: password123')
        self.stdout.write('='*60 + '\n')