import subprocess

def run_password_evaluation(password):
    # Run the evaluator script with the password piped as input
    result = subprocess.run(
        ['python3', 'password_evaluator_score5.py'],
        input=password.encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    output = result.stdout.decode()

    # Try to extract the score from the output text
    for line in output.splitlines():
        if "Security Score" in line:
            try:
                score = int(line.split(":")[1].strip().split("/")[0])
                return score
            except:
                return None
    return None

def evaluate_file(file_path):
    total_score = 0
    count = 0
    print(f"🔍 Reading from: {file_path}")

    with open(file_path, 'r') as file:
        for line in file:
            password = line.strip()
            if password:
                print(f"Evaluating: {password}")

    with open(file_path, 'r') as file:
        for line in file:
            password = line.strip()
            if password:
                score = run_password_evaluation(password)
                if score is not None:
                    print(f"{password:20s} → Score: {score}/5")
                    total_score += score
                    count += 1

    if count > 0:
        avg_score = total_score / count
        print(f"\n✅ Average Score: {avg_score:.2f}/5 across {count} passwords")
    else:
        print("❌ No valid passwords found.")

if __name__ == "__main__":
    evaluate_file("rockyou.txt")
