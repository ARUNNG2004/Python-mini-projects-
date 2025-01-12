import subprocess

def get_wifi_profiles_and_passwords():
    try:
        # Run the command to get Wi-Fi profiles
        output = subprocess.check_output("netsh wlan show profiles", shell=True, text=True)

        # Extract profile names
        profiles = []
        for line in output.splitlines():
            if "All User Profile" in line:
                # Extract the profile name
                profile = line.split(":")[1].strip()
                profiles.append(profile)

        # Retrieve passwords for each profile
        wifi_details = {}
        for profile in profiles:
            try:
                profile_info = subprocess.check_output(
                    f"netsh wlan show profile \"{profile}\" key=clear", shell=True, text=True
                )
                for line in profile_info.splitlines():
                    if "Key Content" in line:
                        # Extract the password
                        password = line.split(":")[1].strip()
                        wifi_details[profile] = password
                        break
                else:
                    wifi_details[profile] = "No password (open network)"
            except subprocess.CalledProcessError:
                wifi_details[profile] = "Error retrieving password"

        return wifi_details

    except subprocess.CalledProcessError as e:
        print("Error retrieving Wi-Fi profiles:", e)
        return {}

# Usage example
if __name__ == "__main__":
    wifi_profiles_passwords = get_wifi_profiles_and_passwords()
    if wifi_profiles_passwords:
        print("Wi-Fi Profiles and Passwords:")
        for profile, password in wifi_profiles_passwords.items():
            print(f"- {profile}: {password}")
    else:
        print("No Wi-Fi profiles found.")
