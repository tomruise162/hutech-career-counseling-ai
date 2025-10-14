import sqlite3
import pandas as pd
import os

def export_sqlite_to_csv():
    """Export data từ SQLite database sang CSV files"""
    
    # Kết nối database
    db_path = r'backend\hutech_consultation.db'
    conn = sqlite3.connect(db_path)
    
    try:
        # 1. Export consultation_sessions
        print("📊 Exporting consultation_sessions...")
        sessions_query = """
        SELECT 
            id,
            student_name,
            student_phone,
            student_email,
            school_name,
            grade,
            score_range,
            riasec_result,
            suggested_majors,
            status,
            created_at,
            ended_at
        FROM consultation_sessions
        ORDER BY created_at DESC
        """
        
        sessions_df = pd.read_sql_query(sessions_query, conn)
        sessions_df.to_csv('consultation_sessions_export.csv', index=False, encoding='utf-8-sig')
        print(f"✅ Exported {len(sessions_df)} sessions to consultation_sessions_export.csv")
        
        # 2. Export consultation_messages
        print("\n💬 Exporting consultation_messages...")
        messages_query = """
        SELECT 
            id,
            session_id,
            role,
            content,
            timestamp
        FROM consultation_messages
        ORDER BY session_id, timestamp
        """
        
        messages_df = pd.read_sql_query(messages_query, conn)
        messages_df.to_csv('consultation_messages_export.csv', index=False, encoding='utf-8-sig')
        print(f"✅ Exported {len(messages_df)} messages to consultation_messages_export.csv")
        
        # 3. Export combined data (sessions + message count)
        print("\n🔗 Exporting combined data...")
        combined_query = """
        SELECT 
            s.id,
            s.student_name,
            s.student_phone,
            s.student_email,
            s.school_name,
            s.grade,
            s.score_range,
            s.riasec_result,
            s.suggested_majors,
            s.status,
            s.created_at,
            s.ended_at,
            COUNT(m.id) as message_count,
            MIN(m.timestamp) as first_message_time,
            MAX(m.timestamp) as last_message_time
        FROM consultation_sessions s
        LEFT JOIN consultation_messages m ON s.id = m.session_id
        GROUP BY s.id
        ORDER BY s.created_at DESC
        """
        
        combined_df = pd.read_sql_query(combined_query, conn)
        combined_df.to_csv('consultation_combined_export.csv', index=False, encoding='utf-8-sig')
        print(f"✅ Exported {len(combined_df)} combined records to consultation_combined_export.csv")
        
        # 4. Export messages with session info
        print("\n📝 Exporting detailed messages...")
        detailed_messages_query = """
        SELECT 
            m.id as message_id,
            m.session_id,
            s.student_name,
            s.grade,
            s.school_name,
            m.role,
            m.content,
            m.timestamp,
            s.created_at as session_start,
            s.ended_at as session_end
        FROM consultation_messages m
        JOIN consultation_sessions s ON m.session_id = s.id
        ORDER BY m.session_id, m.timestamp
        """
        
        detailed_df = pd.read_sql_query(detailed_messages_query, conn)
        detailed_df.to_csv('consultation_detailed_messages_export.csv', index=False, encoding='utf-8-sig')
        print(f"✅ Exported {len(detailed_df)} detailed messages to consultation_detailed_messages_export.csv")
        
        # 5. Show summary
        print("\n📈 SUMMARY:")
        print(f"Total Sessions: {len(sessions_df)}")
        print(f"Total Messages: {len(messages_df)}")
        print(f"Active Sessions: {len(sessions_df[sessions_df['status'] == 'active'])}")
        print(f"Completed Sessions: {len(sessions_df[sessions_df['status'] == 'completed'])}")
        
        # Show latest session info
        if len(sessions_df) > 0:
            latest = sessions_df.iloc[0]
            print(f"\n🕒 Latest Session:")
            print(f"   Student: {latest['student_name']} ({latest['grade']})")
            print(f"   School: {latest['school_name']}")
            print(f"   Started: {latest['created_at']}")
            print(f"   Status: {latest['status']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    finally:
        conn.close()

if __name__ == "__main__":
    export_sqlite_to_csv()
    print("\n🎉 Export completed! Check the CSV files in current directory.")
