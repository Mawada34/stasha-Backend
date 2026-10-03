from db import connection
def init_tables():
    conn=connection()
    cur=conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS portfolio_items(
            id SERIAL PRIMARY KEY,
            title VARCHAR(200) NOT NULL,
            category VARCHAR(50) NOT NULL,
            year INT NOT NULL,
            image_url TEXT NOT NULL,
            display_order INT DEFAULT 0,
            created_at TIMESTAMP DEFAULT NOW()
            );
        """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS testimonials(
            id SERIAL PRIMARY KEY,
            client_name VARCHAR(100) NOT NULL,
            role_location VARCHAR(150),
            project_type VARCHAR(100),
            quote TEXT NOT NULL,
            image_url TEXT NOT NULL,
            display_order INT DEFAULT 0,
            created_at TIMESTAMP DEFAULT NOW()
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS services(
            id SERIAL PRIMARY KEY,
            name VARCHAR (100) NOT NULL,
            description TEXT NOT NULL,
            display_order INT DEFAULT 0
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS hero_content(
            id INT PRIMARY KEY DEFAULT 1,
            headline VARCHAR(200),
            subheadline TEXT,
            video_url TEXT,
            years_count VARCHAR(10),
            projects_count VARCHAR (10),
            satisfaction_pct VARCHAR (10),
            CONSTRAINT single_row CHECK (id=1)
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS about_content(
            id INT PRIMARY KEY DEFAULT 1,
            image_url TEXT,
            paragraph_1 TEXT,
            paragraph_2 TEXT,
            badge_number VARCHAR(10),
            CONSTRAINT single_row CHECK (id=1)
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS site_settings(
            id INT PRIMARY KEY DEFAULT 1,
            booking_url TEXT,
            footer_tagline TEXT,
            instagram_url TEXT,
            pinterest_url TEXT,
            linkedin_url TEXT,
            CONSTRAINT single_row CHECK (id=1)
        );
    """)

    cur.execute ("""
        CREATE TABLE IF NOT EXISTS admin_users(
            id SERIAL PRIMARY KEY,
            email VARCHAR(150) UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT NOW()
        );
    """)

    conn.commit()
    cur.close()
    conn.close()

    print("Database Created Successfully.")

if __name__ == "__main__":
    init_tables()