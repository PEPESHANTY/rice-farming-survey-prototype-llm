import streamlit as st

def collect_user_info():
    professions = [
        "Farmer","Extension Officer","Cooperative" ,"Rice Expert Scientist", "Student", "Agricultural Officer",
        "Researcher", "NGO Representative", "Entrepreneur", "Other"
    ]

    country_state_map = {
        "Vietnam": [
            "An Giang", "Bac Giang", "Bac Kan", "Bac Lieu", "Bac Ninh",
            "Ben Tre", "Binh Dinh", "Binh Duong", "Binh Phuoc",
            "Binh Thuan", "Ca Mau", "Can Tho", "Cao Bang", "Da Nang",
            "Dak Lak", "Dak Nong", "Dien Bien", "Dong Nai", "Dong Thap",
            "Gia Lai", "Ha Giang", "Ha Nam", "Ha Tinh", "Hai Duong",
            "Hai Phong", "Hanoi", "Hau Giang", "Ho Chi Minh City",
            "Hoa Binh", "Hung Yen", "Khanh Hoa", "Kien Giang", "Kon Tum",
            "Lai Chau", "Lam Dong", "Lang Son", "Lao Cai", "Long An",
            "Nam Dinh", "Nghe An", "Ninh Binh", "Ninh Thuan", "Phu Tho",
            "Phu Yen", "Quang Binh", "Quang Nam", "Quang Ngai",
            "Quang Ninh", "Quang Tri", "Soc Trang", "Son La", "Tay Ninh",
            "Thai Binh", "Thai Nguyen", "Thanh Hoa", "Thua Thien-Hue",
            "Tien Giang", "Tra Vinh", "Tuyen Quang", "Vinh Long",
            "Vinh Phuc", "Yen Bai"
        ],
        "Bangladesh": [
            "Barisal", "Chattogram", "Dhaka", "Khulna", "Mymensingh",
            "Rajshahi", "Rangpur", "Sylhet"
        ],
        "Cambodia": [
            "Battambang", "Kampong Cham", "Kampong Chhnang", "Kampong Speu",
            "Kampong Thom", "Kampot", "Kandal", "Koh Kong", "Kratie",
            "Mondulkiri", "Oddar Meanchey", "Pailin", "Phnom Penh",
            "Preah Vihear", "Prey Veng", "Pursat", "Ratanakiri",
            "Siem Reap", "Sihanoukville", "Stung Treng", "Svay Rieng",
            "Takeo", "Tboung Khmum"
        ],
        "India": [
            "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar",
            "Chhattisgarh", "Goa", "Gujarat", "Haryana", "Himachal Pradesh",
            "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh",
            "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland",
            "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu",
            "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand",
            "West Bengal"
        ],
        "Indonesia": [
            "Aceh", "Bali", "Banten", "Bengkulu", "Central Java",
            "Central Kalimantan", "Central Sulawesi", "East Java",
            "East Kalimantan", "East Nusa Tenggara", "Gorontalo",
            "Jakarta", "Jambi", "Lampung", "Maluku", "North Kalimantan",
            "North Maluku", "North Sulawesi", "North Sumatra",
            "Papua", "Riau", "Riau Islands", "Southeast Sulawesi",
            "South Kalimantan", "South Sulawesi", "South Sumatra",
            "West Java", "West Kalimantan", "West Nusa Tenggara",
            "West Papua", "West Sulawesi", "West Sumatra", "Yogyakarta"
        ],
        "Ireland": ["Cork", "Dublin", "Galway", "Limerick", "Waterford","Wicklow"],
        "Laos": [2
                 *
            "Attapeu", "Bokeo", "Bolikhamxai", "Champasak", "Houaphanh",
            "Khammouane", "Luang Namtha", "Luang Prabang", "Oudomxay",
            "Phongsaly", "Salavan", "Savannakhet", "Sekong", "Vientiane",
            "Vientiane Prefecture", "Xaignabouli", "Xaisomboun", "Xieng Khouang"
        ],
        "Myanmar": [
            "Ayeyarwady", "Bago", "Chin", "Kachin", "Kayah", "Kayin",
            "Magway", "Mandalay", "Mon", "Naypyidaw", "Rakhine",
            "Sagaing", "Shan", "Tanintharyi", "Yangon"
        ],
        "Philippines": [
            "Abra", "Agusan del Norte", "Agusan del Sur", "Aklan",
            "Albay", "Antique", "Apayao", "Aurora", "Basilan",
            "Bataan", "Batanes", "Batangas", "Benguet", "Biliran",
            "Bohol", "Bukidnon", "Bulacan", "Cagayan", "Camarines Norte",
            "Camarines Sur", "Camiguin", "Capiz", "Catanduanes",
            "Cavite", "Cebu", "Cotabato", "Davao de Oro", "Davao del Norte",
            "Davao del Sur", "Davao Occidental", "Davao Oriental",
            "Dinagat Islands", "Eastern Samar", "Guimaras", "Ifugao",
            "Ilocos Norte", "Ilocos Sur", "Iloilo", "Isabela", "Kalinga",
            "La Union", "Laguna", "Lanao del Norte", "Lanao del Sur",
            "Leyte", "Maguindanao", "Marinduque", "Masbate", "Metro Manila",
            "Misamis Occidental", "Misamis Oriental", "Mountain Province",
            "Negros Occidental", "Negros Oriental", "Northern Samar",
            "Nueva Ecija", "Nueva Vizcaya", "Occidental Mindoro",
            "Oriental Mindoro", "Palawan", "Pampanga", "Pangasinan",
            "Quezon", "Quirino", "Rizal", "Romblon", "Samar",
            "Sarangani", "Siquijor", "Sorsogon", "South Cotabato",
            "Southern Leyte", "Sultan Kudarat", "Sulu", "Surigao del Norte",
            "Surigao del Sur", "Tarlac", "Tawi-Tawi", "Zambales",
            "Zamboanga del Norte", "Zamboanga del Sur", "Zamboanga Sibugay"
        ],
        "Thailand": [
            "Amnat Charoen", "Ang Thong", "Bangkok", "Bueng Kan",
            "Buriram", "Chachoengsao", "Chai Nat", "Chaiyaphum",
            "Chanthaburi", "Chiang Mai", "Chiang Rai", "Chonburi",
            "Chumphon", "Kalasin", "Kamphaeng Phet", "Kanchanaburi",
            "Khon Kaen", "Krabi", "Lampang", "Lamphun", "Loei",
            "Lopburi", "Mae Hong Son", "Maha Sarakham", "Mukdahan",
            "Nakhon Nayok", "Nakhon Pathom", "Nakhon Phanom",
            "Nakhon Ratchasima", "Nakhon Sawan", "Nakhon Si Thammarat",
            "Nan", "Narathiwat", "Nong Bua Lamphu", "Nong Khai",
            "Nonthaburi", "Pathum Thani", "Pattani", "Phang Nga",
            "Phatthalung", "Phayao", "Phetchabun", "Phetchaburi",
            "Phichit", "Phitsanulok", "Phra Nakhon Si Ayutthaya",
            "Phrae", "Phuket", "Prachinburi", "Prachuap Khiri Khan",
            "Ranong", "Ratchaburi", "Rayong", "Roi Et", "Sa Kaeo",
            "Sakon Nakhon", "Samut Prakan", "Samut Sakhon",
            "Samut Songkhram", "Saraburi", "Satun", "Sing Buri",
            "Sisaket", "Songkhla", "Sukhothai", "Suphan Buri",
            "Surat Thani", "Surin", "Tak", "Trang", "Trat",
            "Ubon Ratchathani", "Udon Thani", "Uthai Thani",
            "Uttaradit", "Yala", "Yasothon"
        ]

    }

    # Title and layout

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("## 🌾 Rice Farming Assistance Agent", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        # Use standard input widgets outside the form to allow real-time reactivity
        name = st.text_input("Name (optional)", key="name_input")
        profession = st.selectbox("Profession", professions, key="profession_input")
        country = st.selectbox("Country", list(country_state_map.keys()), key="country_input")

        # Dynamically update states
        states = country_state_map.get(country, [])
        state = st.selectbox("State", states, key="state_input")

        if st.button("Continue to Chat▶️"):
            final_name = name.strip() if name.strip() else "User"
            st.session_state["user_metadata"] = {
                "name": final_name,
                "profession": profession,
                "country": country,
                "state": state
            }
            st.session_state["show_chat"] = True
