import os
import src.database as db
import src.llm as llm

print("Current Working Directory:", os.getcwd())

# 1. Verify Imports
print("✅ Imports successful")

# 2. Verify DB Creation
if os.path.exists("feedback.db"):
    os.remove("feedback.db")

db.init_db()
if os.path.exists("feedback.db"):
    print("✅ Database file created successfully")
else:
    print("❌ Database creation failed")

# 3. Verify DB Insert/Fetch
try:
    db.save_submission(5, "Test Review", "Response", "Summary", "Reco")
    df = db.fetch_all_submissions()
    if len(df) == 1:
        print("✅ Database insert/fetch successful")
    else:
        print(f"❌ Database insert/fetch mismatch: {len(df)}")
except Exception as e:
    print(f"❌ Database error: {e}")

# 4. Verify LLM configuration (Graceful fail check)
try:
    # This should return a default message or error string if no key, but not crash
    response = llm.generate_user_response(5, "Test")
    print(f"✅ LLM Handler called successfully (Response: {response[:30]}...)")
except Exception as e:
    print(f"❌ LLM Handler crashed: {e}")
