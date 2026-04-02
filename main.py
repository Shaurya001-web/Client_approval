/*
 * =====================================================
 *  Simple Client Document Approval System
 *  1st Year B.Tech College Project
 *  Team Project | College Submission
 * =====================================================
 *
 *  CONCEPTS USED (all 1st year syllabus):
 *  - Structs
 *  - Arrays
 *  - Functions
 *  - Loops (for, while)
 *  - Switch-case
 *  - If-else
 *  - cin / cout
 *  - String basics
 *
 *  HOW TO COMPILE & RUN IN VS CODE:
 *    g++ -o project main.cpp
 *    ./project         (Linux/Mac)
 *    project.exe       (Windows)
 *
 *  TEAM SPLIT SUGGESTION (4 members):
 *    Member 1 -> Login system (lines ~60-120)
 *    Member 2 -> Document upload & display (lines ~120-200)
 *    Member 3 -> Approval workflow (lines ~200-270)
 *    Member 4 -> Comments & report (lines ~270-350)
 * =====================================================
 */

#include <iostream>
#include <string>
using namespace std;

// ─────────────────────────────────────────
//  CONSTANTS
// ─────────────────────────────────────────
const int MAX_USERS     = 10;
const int MAX_DOCS      = 20;
const int MAX_COMMENTS  = 5;   // comments per document

// ─────────────────────────────────────────
//  STRUCTS  (like a simple database row)
// ─────────────────────────────────────────

class User {
    public:
    string name;
    string email;
    string password;
    string role;       // "admin" or "client"
    bool   active;     // is this slot used?
};

class Comment {
    public:
    string author;
    string text;
    bool   used;
};

class Document {
    public:
    int    id;
    string title;
    string description;
    string filename;
    string uploaded_by;
    string status;         // "Pending", "Approved", "Changes Requested"
    Comment comments[MAX_COMMENTS];
    int    comment_count;
    bool   active;
};

// ─────────────────────────────────────────
//  GLOBAL DATA  (our in-memory "database")
// ─────────────────────────────────────────
User     users[MAX_USERS];
Document docs[MAX_DOCS];
int      user_count = 0;
int      doc_count  = 0;
int      doc_id_counter = 1;

// Currently logged-in user (-1 means nobody)
int current_user_index = -1;

// ─────────────────────────────────────────
//  UTILITY FUNCTIONS
// ─────────────────────────────────────────

// Print a divider line
void divider() {
    cout << "\n------------------------------------------\n";
}

// Print the app header
void printHeader() {
    cout << "\n==========================================\n";
    cout << "   CLIENT DOCUMENT APPROVAL PORTAL\n";
    cout << "==========================================\n";
}

// Pause until user presses Enter
void pause() {
    cout << "\nPress Enter to continue...";
    cin.ignore();
    cin.get();
}

// Check if a string is empty
bool isEmpty(string s) {
    return s.length() == 0;
}

// ─────────────────────────────────────────
//  MEMBER 1: LOGIN SYSTEM
// ─────────────────────────────────────────

// Add demo users when program starts
void seedUsers() {
    // Admin user
    users[0].name     = "Admin User";
    users[0].email    = "admin@portal.com";
    users[0].password = "admin123";
    users[0].role     = "admin";
    users[0].active   = true;

    // Client user
    users[1].name     = "Acme Corp";
    users[1].email    = "client@acme.com";
    users[1].password = "client123";
    users[1].role     = "client";
    users[1].active   = true;

    user_count = 2;
}

// Add a demo document so there is something to see on first run
void seedDocuments() {
    docs[0].id           = doc_id_counter++;
    docs[0].title        = "Q1 Campaign Proposal";
    docs[0].description  = "Marketing campaign plan for Q1";
    docs[0].filename     = "q1_campaign.pdf";
    docs[0].uploaded_by  = "Admin User";
    docs[0].status       = "Pending";
    docs[0].comment_count = 0;
    docs[0].active       = true;

    docs[1].id           = doc_id_counter++;
    docs[1].title        = "Website Redesign Mockup";
    docs[1].description  = "New website UI mockups for review";
    docs[1].filename     = "mockup_v2.pdf";
    docs[1].uploaded_by  = "Admin User";
    docs[1].status       = "Changes Requested";
    docs[1].comment_count = 1;
    docs[1].comments[0].author = "Acme Corp";
    docs[1].comments[0].text   = "Please change the color scheme.";
    docs[1].comments[0].used   = true;
    docs[1].active       = true;

    doc_count = 2;
}

// Try to log in — returns user index if found, -1 if not
int loginUser(string email, string password) {
    for (int i = 0; i < MAX_USERS; i++) {
        if (users[i].active &&
            users[i].email    == email &&
            users[i].password == password) {
            return i;
        }
    }
    return -1;  // not found
}

// Register a brand new user
void registerUser() {
    if (user_count >= MAX_USERS) {
        cout << "  [!] User limit reached.\n";
        return;
    }

    cout << "\n  --- REGISTER NEW ACCOUNT ---\n";
    string name, email, password, role;

    cout << "  Full Name   : "; cin.ignore(); getline(cin, name);
    cout << "  Email       : "; getline(cin, email);
    cout << "  Password    : "; getline(cin, password);
    cout << "  Role (admin/client): "; getline(cin, role);

    if (isEmpty(name) || isEmpty(email) || isEmpty(password)) {
        cout << "  [!] All fields are required.\n";
        return;
    }
    if (role != "admin" && role != "client") role = "client";

    // Check duplicate email
    for (int i = 0; i < MAX_USERS; i++) {
        if (users[i].active && users[i].email == email) {
            cout << "  [!] Email already registered.\n";
            return;
        }
    }

    users[user_count].name     = name;
    users[user_count].email    = email;
    users[user_count].password = password;
    users[user_count].role     = role;
    users[user_count].active   = true;
    user_count++;

    cout << "  [✓] Account created! You can now log in.\n";
}

// The login screen shown at startup
bool loginScreen() {
    divider();
    cout << "  1. Login\n";
    cout << "  2. Register\n";
    cout << "  3. Exit\n";
    cout << "  Choice: ";

    int choice;
    cin >> choice;

    if (choice == 3) return false;  // exit program

    if (choice == 2) {
        registerUser();
        return true;
    }

    // Default: Login
    cout << "\n  Email    : "; cin.ignore(); 
    string email; getline(cin, email);
    cout << "  Password : ";
    string password; getline(cin, password);

    int idx = loginUser(email, password);
    if (idx == -1) {
        cout << "  [!] Wrong email or password.\n";
        pause();
    } else {
        current_user_index = idx;
        cout << "\n  [✓] Welcome, " << users[idx].name
             << "! (" << users[idx].role << ")\n";
        pause();
    }
    return true;
}

// ─────────────────────────────────────────
//  MEMBER 2: DOCUMENT UPLOAD & DISPLAY
// ─────────────────────────────────────────

// Find a document by its ID
int findDocById(int id) {
    for (int i = 0; i < MAX_DOCS; i++) {
        if (docs[i].active && docs[i].id == id)
            return i;
    }
    return -1;
}

// Print one document as a summary row
void printDocRow(Document& d) {
    cout << "  [" << d.id << "] " << d.title
         << " | Status: " << d.status
         << " | By: " << d.uploaded_by << "\n";
}

// List all documents
void listDocuments() {
    divider();
    cout << "  ALL DOCUMENTS\n";
    divider();

    bool any = false;
    for (int i = 0; i < MAX_DOCS; i++) {
        if (docs[i].active) {
            printDocRow(docs[i]);
            any = true;
        }
    }
    if (!any) cout << "  No documents yet.\n";
    pause();
}

// View full detail of one document
void viewDocument() {
    cout << "\n  Enter Document ID: ";
    int id; cin >> id;

    int idx = findDocById(id);
    if (idx == -1) { cout << "  [!] Document not found.\n"; pause(); return; }

    Document& d = docs[idx];
    divider();
    cout << "  DOCUMENT DETAIL\n";
    divider();
    cout << "  ID          : " << d.id << "\n";
    cout << "  Title       : " << d.title << "\n";
    cout << "  Description : " << d.description << "\n";
    cout << "  Filename    : " << d.filename << "\n";
    cout << "  Uploaded By : " << d.uploaded_by << "\n";
    cout << "  Status      : " << d.status << "\n";

    cout << "\n  Comments (" << d.comment_count << "):\n";
    if (d.comment_count == 0) {
        cout << "    (none yet)\n";
    } else {
        for (int i = 0; i < MAX_COMMENTS; i++) {
            if (docs[idx].comments[i].used) {
                cout << "    [" << docs[idx].comments[i].author << "]: "
                     << docs[idx].comments[i].text << "\n";
            }
        }
    }
    pause();
}

// Upload a new document (admin only)
void uploadDocument() {
    if (users[current_user_index].role != "admin") {
        cout << "  [!] Only admins can upload documents.\n";
        pause(); return;
    }
    if (doc_count >= MAX_DOCS) {
        cout << "  [!] Document limit reached.\n";
        pause(); return;
    }

    cout << "\n  --- UPLOAD NEW DOCUMENT ---\n";
    string title, desc, filename;

    cin.ignore();
    cout << "  Title       : "; getline(cin, title);
    cout << "  Description : "; getline(cin, desc);
    cout << "  Filename    : "; getline(cin, filename);

    if (isEmpty(title) || isEmpty(filename)) {
        cout << "  [!] Title and filename are required.\n";
        pause(); return;
    }

    // Find empty slot
    for (int i = 0; i < MAX_DOCS; i++) {
        if (!docs[i].active) {
            docs[i].id            = doc_id_counter++;
            docs[i].title         = title;
            docs[i].description   = desc;
            docs[i].filename      = filename;
            docs[i].uploaded_by   = users[current_user_index].name;
            docs[i].status        = "Pending";
            docs[i].comment_count = 0;
            docs[i].active        = true;
            doc_count++;
            cout << "  [✓] Document uploaded! ID = " << docs[i].id << "\n";
            pause();
            return;
        }
    }
}

// ─────────────────────────────────────────
//  MEMBER 3: APPROVAL WORKFLOW
// ─────────────────────────────────────────

// Change the status of a document
void changeDocumentStatus() {
    cout << "\n  Enter Document ID: ";
    int id; cin >> id;

    int idx = findDocById(id);
    if (idx == -1) { cout << "  [!] Document not found.\n"; pause(); return; }

    cout << "\n  Current Status: " << docs[idx].status << "\n";
    cout << "  Choose new status:\n";
    cout << "    1. Approved\n";
    cout << "    2. Changes Requested\n";
    cout << "    3. Pending\n";
    cout << "  Choice: ";

    int ch; cin >> ch;
    switch (ch) {
        case 1: docs[idx].status = "Approved";           break;
        case 2: docs[idx].status = "Changes Requested";  break;
        case 3: docs[idx].status = "Pending";            break;
        default: cout << "  [!] Invalid choice.\n"; pause(); return;
    }

    cout << "  [✓] Status updated to: " << docs[idx].status << "\n";
    pause();
}

// Delete a document (admin only)
void deleteDocument() {
    if (users[current_user_index].role != "admin") {
        cout << "  [!] Only admins can delete documents.\n";
        pause(); return;
    }

    cout << "\n  Enter Document ID to delete: ";
    int id; cin >> id;

    int idx = findDocById(id);
    if (idx == -1) { cout << "  [!] Document not found.\n"; pause(); return; }

    docs[idx].active = false;
    doc_count--;
    cout << "  [✓] Document deleted.\n";
    pause();
}

// ─────────────────────────────────────────
//  MEMBER 4: COMMENTS & REPORT
// ─────────────────────────────────────────

// Add a comment to a document
void addComment() {
    cout << "\n  Enter Document ID: ";
    int id; cin >> id;

    int idx = findDocById(id);
    if (idx == -1) { cout << "  [!] Document not found.\n"; pause(); return; }
    if (docs[idx].comment_count >= MAX_COMMENTS) {
        cout << "  [!] Comment limit reached for this document.\n";
        pause(); return;
    }

    string text;
    cin.ignore();
    cout << "  Your comment: "; getline(cin, text);

    if (isEmpty(text)) { cout << "  [!] Comment cannot be empty.\n"; pause(); return; }

    // Find empty comment slot
    for (int i = 0; i < MAX_COMMENTS; i++) {
        if (!docs[idx].comments[i].used) {
            docs[idx].comments[i].author = users[current_user_index].name;
            docs[idx].comments[i].text   = text;
            docs[idx].comments[i].used   = true;
            docs[idx].comment_count++;
            cout << "  [✓] Comment added.\n";
            pause();
            return;
        }
    }
}

// Print a summary report of all documents
void printReport() {
    divider();
    cout << "  SUMMARY REPORT\n";
    divider();

    int pending = 0, approved = 0, changes = 0;
    for (int i = 0; i < MAX_DOCS; i++) {
        if (!docs[i].active) continue;
        if      (docs[i].status == "Pending")           pending++;
        else if (docs[i].status == "Approved")          approved++;
        else if (docs[i].status == "Changes Requested") changes++;
    }

    cout << "  Total Documents    : " << doc_count   << "\n";
    cout << "  Pending Review     : " << pending     << "\n";
    cout << "  Approved           : " << approved    << "\n";
    cout << "  Changes Requested  : " << changes     << "\n";
    cout << "  Total Users        : " << user_count  << "\n";
    divider();
    pause();
}

// ─────────────────────────────────────────
//  MAIN MENU (after login)
// ─────────────────────────────────────────
void mainMenu() {
    while (true) {
        printHeader();
        cout << "  Logged in as: " << users[current_user_index].name
             << " (" << users[current_user_index].role << ")\n";
        divider();
        cout << "  1. List All Documents\n";
        cout << "  2. View Document Detail\n";
        cout << "  3. Change Document Status (Approve/Reject)\n";
        cout << "  4. Add Comment to Document\n";
        cout << "  5. Print Summary Report\n";
        if (users[current_user_index].role == "admin") {
            cout << "  6. Upload New Document  [Admin]\n";
            cout << "  7. Delete Document      [Admin]\n";
        }
        cout << "  0. Logout\n";
        cout << "\n  Choice: ";

        int ch; cin >> ch;
        switch (ch) {
            case 1: listDocuments();       break;
            case 2: viewDocument();        break;
            case 3: changeDocumentStatus(); break;
            case 4: addComment();          break;
            case 5: printReport();         break;
            case 6:
                if (users[current_user_index].role == "admin") uploadDocument();
                break;
            case 7:
                if (users[current_user_index].role == "admin") deleteDocument();
                break;
            case 0:
                current_user_index = -1;
                cout << "  [✓] Logged out.\n";
                return;
            default:
                cout << "  [!] Invalid choice.\n";
        }
    }
}

// ─────────────────────────────────────────
//  MAIN
// ─────────────────────────────────────────
int main() {
    // Load demo data
    seedUsers();
    seedDocuments();

    printHeader();
    cout << "\n  Demo Accounts:\n";
    cout << "  Admin  -> admin@portal.com  / admin123\n";
    cout << "  Client -> client@acme.com   / client123\n";

    // Keep showing login screen until user logs in or exits
    while (true) {
        if (current_user_index == -1) {
            bool keepGoing = loginScreen();
            if (!keepGoing) break;
        } else {
            mainMenu();
        }
    }

    cout << "\n  Goodbye! Thank you for using the portal.\n\n";
    return 0;
}
