

```python
class Book:
  def __init__(self, book_id, available_copies):
    self.book_id = book_id
    self.available_copies = available_copies
  def update_available_copies(self, change):
    self.available_copies += change
  def __repr__(self):
    return f'Book(book_id={self.book_id}, available_copies={self.available_copies})'
```