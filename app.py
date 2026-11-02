from flask import Flask, request, jsonify, abort, render_template_string

app = Flask(__name__)

# Hard-coded book data
books = [
    {"id": 1, "title": "1984", "author": "George Orwell", "rating": 4.9},
    {"id": 2, "title": "Brave New World", "author": "Aldous Huxley", "rating": 4.3},
    {"id": 3, "title": "Fahrenheit 451", "author": "Ray Bradbury", "rating": 4.7},
    {"id": 4, "title": "Things Fall Apart", "author": "Chinua Achebe", "rating": 5.0},
]


# Welcome endpoint
@app.route("/")
def welcome():
    return jsonify(message="Welcome to Tiny REST App!")


# GET all books
@app.route("/goodbooks", methods=["GET"])
def get_books():
    return jsonify(books)


# GET a book by ID
@app.route("/goodbooks/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    if not book:
        abort(404, description="Book not found")
    return jsonify(book)


# POST a new book
@app.route("/goodbooks", methods=["POST"])
def add_book():
    data = request.get_json(silent=True)
    if not isinstance(data, dict) or "title" not in data or "author" not in data:
        abort(400, description="Missing required fields")

    rating = data.get("rating", 0)
    if (
        not isinstance(rating, (int, float))
        or isinstance(rating, bool)
        or not 1 <= rating <= 5
    ):
        abort(400, description="Rating must be between 1 and 5")

    new_id = max(b["id"] for b in books) + 1 if books else 1
    book = {
        "id": new_id,
        "title": data["title"],
        "author": data["author"],
        "rating": rating,
    }
    books.append(book)
    return jsonify(book), 201


# PUT update a book
@app.route("/goodbooks/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        abort(400, description="Invalid JSON data")

    book = next((b for b in books if b["id"] == book_id), None)
    if not book:
        abort(404, description="Book not found")

    if "rating" in data:
        rating = data["rating"]
        if (
            not isinstance(rating, (int, float))
            or isinstance(rating, bool)
            or not 1 <= rating <= 5
        ):
            abort(400, description="Rating must be between 1 and 5")

    book.update({k: v for k, v in data.items() if k in ["title", "author", "rating"]})
    return jsonify(book)


# DELETE a book
@app.route("/goodbooks/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    global books
    if not any(b["id"] == book_id for b in books):
        abort(404, description="Book not found")
    books = [b for b in books if b["id"] != book_id]
    return "", 204


# Dynamic HTML table with conditional formatting
TABLE_TEMPLATE = """
<!doctype html>
<html>
<head>
    <title>Good Books</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        table { border-collapse: collapse; width: 80%; }
        th, td { border: 1px solid #ccc; padding: 12px; text-align: left; }
        th { background-color: #eee; }
        .high-rating { background-color: lightgreen; }
        .error { color: darkred; }
    </style>
</head>
<body>
    <h1>Good Books</h1>
    <p id="status">Loading books...</p>
    <table id="books-table" hidden>
        <thead>
            <tr><th>ID</th><th>Title</th><th>Author</th><th>Rating</th></tr>
        </thead>
        <tbody id="books-body"></tbody>
    </table>
    <script>
        async function loadBooks() {
            const status = document.getElementById('status');
            const table = document.getElementById('books-table');
            const body = document.getElementById('books-body');
            try {
                const response = await fetch('/goodbooks');
                if (!response.ok) throw new Error('HTTP ' + response.status);
                const books = await response.json();
                body.replaceChildren();

                books.forEach(book => {
                    const row = document.createElement('tr');
                    if (book.rating >= 4) row.className = 'high-rating';
                    ['id', 'title', 'author', 'rating'].forEach(field => {
                        const cell = document.createElement('td');
                        cell.textContent = book[field];
                        row.appendChild(cell);
                    });
                    body.appendChild(row);
                });

                status.hidden = true;
                table.hidden = false;
            } catch (error) {
                table.hidden = true;
                status.hidden = false;
                status.className = 'error';
                status.textContent = 'Unable to load books: ' + error.message;
            }
        }
        loadBooks();
    </script>
</body>
</html>
"""


@app.route("/goodbooks/html")
def books_html():
    return render_template_string(TABLE_TEMPLATE)


if __name__ == "__main__":
    app.run(debug=True)
