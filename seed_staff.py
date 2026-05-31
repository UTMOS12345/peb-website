from app import Staff, app, db

# Updated with full names from the school database and crop adjustments
staff_data = [
    {
        "name": "Abdumalik Berdimuradov", 
        "full_name": "Berdimuradov Abdumalik Azamatovich",
        "role": "General Manager", 
        "dept": "Executive Council", 
        "initial": "A", 
        "img": "https://api.alberuni.uz/storage/01K7181W4DPJTNQ84XXTG8WZ7N.jpg", # Paste link here
        "pos": "center"
    },
    {
        "name": "Kamila Mirzayeva", 
        "full_name": "Mirzayeva Kamila Dilmurodovna",
        "role": "Council Manager / Media Manager", 
        "dept": "Executive Council", 
        "initial": "K", 
        "img": "https://api.alberuni.uz/storage/01K6ZF04Q9G840W41PDWSB200S.jpg", 
        "pos": "center"
    },
    {
        "name": "Mushtariy Abdusamadova", 
        "full_name": "Abdusamadova Mushtariy Akmal qizi",
        "role": "Finance Manager", 
        "dept": "Executive Council", 
        "initial": "M", 
        "img": "https://api.alberuni.uz/storage/01K719TNS6E7Q7QXJ9MN5SQYPT.jpg", 
        "pos": "center"
    },
    {
        "name": "Behruz Asrorov", 
        "full_name": "Asrorov Behruz Abror o'g'li",
        "role": "Finance Manager", 
        "dept": "Executive Council", 
        "initial": "B", 
        "img": "https://api.alberuni.uz/storage/01K71JB98Z7X1SB5DTSGNJ6BFA.jpg", 
        "pos": "center"
    },
    {
        "name": "Eldor Akbaraliyev", 
        "full_name": "Akbaraliyev Eldorbek Elyor o'g'li",
        "role": "Media Manager", 
        "dept": "Executive Council", 
        "initial": "E", 
        "img": "https://api.alberuni.uz/storage/01K719FNGC2G6YQ7K6G026JE50.jpg", 
        "pos": "center"
    },
    {
        "name": "Gulnoza Gulmuratova", 
        "full_name": "Gulmuratova Gulnoza Ong'arbay qizi",
        "role": "Network Manager", 
        "dept": "Executive Council", 
        "initial": "G", 
        "img": "https://api.alberuni.uz/storage/01K6ZF98TEV6Q0057Y20RXX51K.jpg", 
        "pos": "center"
    },
    {
        "name": "Shahina To'ychiyeva", 
        "full_name": "To'ychiyeva Shahina Sherzodovna",
        "role": "Event Organizer", 
        "dept": "Events and External Relations Council", 
        "initial": "S", 
        "img": "https://api.alberuni.uz/storage/01K71KE3FAW4ZZWCB8ZYE0VZFE.jpg", 
        "pos": "center"
    },
    {
        "name": "Feruzbek Numonjonov", 
        "full_name": "Nu'monjonov Feruzbek Nodirbek o'g'li",
        "role": "Event Organizer", 
        "dept": "Events and External Relations Council", 
        "initial": "F", 
        "img": "", 
        "pos": "center"
    },
    {
        "name": "Shodiyona Olimjonova", 
        "full_name": "Olimjonova Shodiyona Erkin qizi",
        "role": "Event Organizer", 
        "dept": "Events and External Relations Council", 
        "initial": "S", 
        "img": "", 
        "pos": "center"
    },
    {
        "name": "Maryam Ibragimova", 
        "full_name": "Ibragimova Maryam Ulug'bekovna",
        "role": "Editor Chief", 
        "dept": "Publications and Research Council", 
        "initial": "M", 
        "img": "", 
        "pos": "center"
    },
    {
        "name": "Sarvar Faxriddinov", 
        "full_name": "Faxriddinov Sarvarjon Anvarjon o'g'li",
        "role": "Editor Chief", 
        "dept": "Publications and Research Council", 
        "initial": "S", 
        "img": "", 
        "pos": "center"
    },
    {
        "name": "Javlon Mingboyev", 
        "full_name": "Mingboyev Javlonbek Alisherovich",
        "role": "Research Coordinator", 
        "dept": "Publications and Research Council", 
        "initial": "J", 
        "img": "https://api.alberuni.uz/storage/01K71WP7B5XQZ9E9PD78VB9WWH.jpg", 
        "pos": "center"
    },
    {
        "name": "Jaloliddin Qurbonov", 
        "full_name": "Qurbonov Jaloliddin Kamoliddinovich",
        "role": "Web Designer", 
        "dept": "Publications and Research Council", 
        "initial": "J", 
        "img": "https://api.alberuni.uz/storage/01K717RAZ5HR4M5RE2616CT7BV.jpg", 
        "pos": "center"
    },
    {
        "name": "Maksudali Imoaliyev ", 
        "full_name": "Imomaliyev Maqsudali Hasanboyevich",
        "role": "Web Designer & Backend Programmer", 
        "dept": "Publications and Research Council", 
        "initial": "I'M", 
        "img": "", 
        "pos": "left" # Adjusted position for crop fix
    },
    {
        "name": "Daler Nozimov", 
        "full_name": "Nozimov Daler Nuraliyevich",
        "role": "MUN President", 
        "dept": "MUN Department", 
        "initial": "D", 
        "img": "https://api.alberuni.uz/storage/01K6ZF4S9KFG1W6XMY15M2B6JK.jpg", 
        "pos": "center"
    },
    {
        "name": "Nilufar Umarova", 
        "full_name": "Umarova Nilufar Shukurilla qizi",
        "role": "MUN Vice-President", 
        "dept": "MUN Department", 
        "initial": "N", 
        "img": "https://api.alberuni.uz/storage/01K7176SR7Q63VDGYXHVA54D46.jpg", 
        "pos": "center"
    },
]

def run_update():
    with app.app_context():
        print("Wiping old staff data...")
        db.session.query(Staff).delete()

        for s in staff_data:
            # We use the friendly name but you can use s['full_name'] if preferred
            new_staff = Staff(
                name=s["name"], 
                role=s["role"],
                department=s["dept"],
                initial=s["initial"],
                image_url=s["img"],
                image_position=s["pos"]
            )
            db.session.add(new_staff)

        db.session.commit()
        print(f"Success! Planted {len(staff_data)} staff members.")

if __name__ == "__main__":
    run_update()
