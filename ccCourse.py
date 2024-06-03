import firebase_admin
from firebase_admin import credentials , firestore
import streamlit as st
import pandas as pd
import datetime

cred = credentials.Certificate("cloudcomputing-7dbb6-firebase-adminsdk-noc16-a0f0816021.json")
#firebase_admin.initialize_app(cred)

db = firestore.client()

# users = [
#     {
#         "student_name": "Vedant",
#         "clg_id": "1234567890",
#         "study_years": "2021"
#     },
#     {
#         "student_name": "Advait",
#         "clg_id": "0987654321",
#         "study_years": "2022"
#     },
#     {
#         "student_name": "Leander",
#         "clg_id": "4567890123",
#         "study_years": "2023"
#     },
#     {
#         "student_name": "Shivaraj",
#         "clg_id": "3210987654",
#         "study_years": "2024"
#     },
#     {
#         "student_name": "Dhrub",
#         "clg_id": "9876543210",
#         "study_years": "2025"
#     },
#     {
#         "student_name": "Pratik",
#         "clg_id": "5678901234",
#         "study_years": "2021"
#     },
#     {
#         "student_name": "Irfan",
#         "clg_id": "2345678901",
#         "study_years": "2022"
#     },
#     {
#         "student_name": "Chaitanya",
#         "clg_id": "1098765432",
#         "study_years": "2023"
#     },
#     {
#         "student_name": "Prathmesh",
#         "clg_id": "8901234567",
#         "study_years": "2024"
#     },
#     {
#         "student_name": "Prashant",
#         "clg_id": "4321098765",
#         "study_years": "2025"
#     }
# ]

# for user in users:
#     db.collection("users").add(user)

# print("Data added successfully.")

# books = [
#     {
#         "Name": "Book 1",
#         "Author": "Author 1",
#         "Genre": "Genre 1",
#         "Quantity": 5
#     },
#     {
#         "Name": "Book 2",
#         "Author": "Author 2",
#         "Genre": "Genre 2",
#         "Quantity": 3
#     },
#     {
#         "Name": "Book 3",
#         "Author": "Author 3",
#         "Genre": "Genre 3",
#         "Quantity": 7
#     },
#     {
#         "Name": "Book 4",
#         "Author": "Author 4",
#         "Genre": "Genre 1",
#         "Quantity": 2
#     },
#     {
#         "Name": "Book 5",
#         "Author": "Author 5",
#         "Genre": "Genre 2",
#         "Quantity": 4
#     },
#     {
#         "Name": "Book 6",
#         "Author": "Author 6",
#         "Genre": "Genre 3",
#         "Quantity": 6
#     },
#     {
#         "Name": "Book 7",
#         "Author": "Author 7",
#         "Genre": "Genre 1",
#         "Quantity": 8
#     },
#     {
#         "Name": "Book 8",
#         "Author": "Author 8",
#         "Genre": "Genre 2",
#         "Quantity": 1
#     },
#     {
#         "Name": "Book 9",
#         "Author": "Author 9",
#         "Genre": "Genre 3",
#         "Quantity": 10
#     },
#     {
#         "Name": "Book 10",
#         "Author": "Author 10",
#         "Genre": "Genre 1",
#         "Quantity": 3
#     }
# ]

# for book in books:
#     db.collection("books").add(book)
def fetch_books():
    books = db.collection("books").get()
    bookList = []
    for book in books:
        book_data = {
            "Name": book.get("Name"),
            "Author": book.get("Author"),
            "Genre": book.get("Genre"),
            "Quantity": book.get("Quantity")
        }
        bookList.append(book_data)
    return bookList

def login(username):

    
    query = db.collection("users").where("student_name", "==", username).limit(1).get()
    for doc in query:
        stored_clg_id = doc.get("clg_id")

    return stored_clg_id

def fetch_book_requests():
    requests = db.collection("book_requests").get()
    request_list = []
    for request in requests:
        request_data = {
            "Name": request.get("Name"),
            "bookname": request.get("bookname"),
            "assign_date": request.get("assign_date"),
            "return_date": request.get("return_date")
        }
        request_list.append(request_data)
    return request_list

def make_book_request(username,book_name,assign_date,return_date):

    if not username:
        st.warning("PLease Log in first")
        return

    data={
    "Name": username ,
    "bookname":book_name,
    "assign_date": assign_date.isoformat(),
    "return_date": return_date.isoformat()
    }

    db.collection("book_requests").add(data)
    st.success("Request sent successfully!")

def user_login(username, password):
    query = db.collection("users").where("student_name", "==", username).limit(1).get()
    for doc in query:
        stored_clg_id = doc.get("clg_id")
    if stored_clg_id :
        return stored_clg_id == password
    return False

def userbooks(coll):
    books = db.collection(coll).get() 
    user_books = []
    for doc in books:
        book_data = {
            "bookname": doc.get("bookname"),
            "assign_date": doc.get("assign_date"),
            "return_date": doc.get("return_date")
        }
        user_books.append(book_data)

    return user_books

def main():

    
    
    st.title("Library")


    selection = st.sidebar.radio("Navigation", ["User", "Admin"])

    if selection == "Admin":
        st.header("Admin Panel")
        password = st.text_input("Enter Admin Password", type="password")
        
        if password == "admin1234":

            st.header("Add Books")

            Name = st.text_input("Name")
            Author = st.text_input("Author")
            Genre = st.text_input("Genre")
            Quantity = st.number_input("Quantity", min_value=0)

            if st.button("Submit"):
                data= {
                "Name": Name,
                "Author":Author,
                "Genre": Genre ,
                "Quantity": Quantity
                }
                db.collection("books").add(data)
                st.success("Book added successfully!")

            st.header("Book Requests")
            requests = fetch_book_requests()
            if requests:
                for request in requests:
                
                    st.write(f"Name: {request['Name']}")
                    st.write(f"Book Name: {request['bookname']}")
                    st.write(f"Assign Date: {request['assign_date']}")
                    st.write(f"Return Date: {request['return_date']}")

                    if st.button(f"Assign Book {request['bookname']}"):
                        data={
                          "bookname": request['bookname'],
                          "assign_date": request['assign_date'],
                          "return_date": request['return_date']
                        }
                        table=request['Name']+"_books"
                        db.collection(table).add(data)

                    
                        query = db.collection("books").where("Name", "==",request['bookname'] ).limit(1).get()
                        for doc in query:
            
                            current_quantity = doc.get("Quantity")
                            new_quantity = current_quantity - 1
                            doc_ref = db.collection("books").document(doc.id)
                            doc_ref.update({"Quantity": new_quantity})

                        request_query = db.collection("book_requests").where("bookname", "==", request['bookname']).limit(1).get()
                        for request_doc in request_query:
    
                            request_doc_ref = db.collection("book_requests").document(request_doc.id)
                            request_doc_ref.delete()

                        st.success("Book Assigned Sucessfully")
            else:
                st.write("No book requests found.")

    elif selection == "User":

        st.header("User Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if user_login(username, password):
                st.success("Login successful!")
                coll= username+"_books"
                user_books=userbooks(coll)

                st.title("Assigned books")
        
        
        
                if user_books:
            
                    df2 = pd.DataFrame(user_books)
                    st.dataframe(df2)
                else:
                    st.write("No user books found.")

        # username= "Vedant"    
        st.title("Available Books")
        books = fetch_books()
        if books:
            st.write("List of Books:")
            df = pd.DataFrame(books)
            st.dataframe(df)
        else:
            st.write("No books found.")
        st.header("Make Book Assignment Request")
        
        book_name = st.text_input("Book Name")
        assign_date = st.date_input("Assign Date")
        return_date = st.date_input("Return Date")
        if st.button("Send Request"):
            make_book_request(username, book_name, assign_date, return_date)
            



if __name__ == "__main__":
    main()



