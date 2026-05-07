
class PageOutOfRangeError(Exception):
    def __init__(self, book_total, trans_pages):
        self.book_total = book_total
        self.trans_pages = trans_pages
        super().__init__(f"指定的页数 {trans_pages} 超过PDF总页数 {book_total}")

# if __name__ == "__main__":
#     try:
#         raise PageOutOfRangeError(10, 15)
#     except PageOutOfRangeError as e:
#         print(e)