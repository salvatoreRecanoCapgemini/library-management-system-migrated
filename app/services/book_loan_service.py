

package app.services;

import app.repositories.BookRepository;
import app.repositories.LoanRepository;
import app.repositories.PatronRepository;
import app.exceptions.BookNotAvailableException;
import app.exceptions.PatronAccountNotActiveException;
import app.exceptions.PatronMaxLoansReachedException;
import app.exceptions.DatabaseOperationException;

public class BookLoanService {
    private BookRepository bookRepository;
    private LoanRepository loanRepository;
    private PatronRepository patronRepository;

    public BookLoanService(BookRepository bookRepository, LoanRepository loanRepository, PatronRepository patronRepository) {
        this.bookRepository = bookRepository;
        this.loanRepository = loanRepository;
        this.patronRepository = patronRepository;
    }

    public int processBookLoan(int patronId, int bookId, int loanDays) {
        if (patronId <= 0 || bookId <= 0 || loanDays <= 0) {
            throw new IllegalArgumentException("Invalid input parameters");
        }

        try {
            int availableCopies = bookRepository.getBookAvailability(bookId);
            if (availableCopies <= 0) {
                throw new BookNotAvailableException("Book is not available for loan");
            }

            String patronStatus = patronRepository.getPatronStatus(patronId);
            int activeLoans = patronRepository.getActiveLoans(patronId);
            if (!patronStatus.equals("ACTIVE")) {
                throw new PatronAccountNotActiveException("Patron account is not active");
            }
            if (activeLoans >= 5) {
                throw new PatronMaxLoansReachedException("Patron has reached maximum number of loans");
            }

            int loanId = loanRepository.createLoanRecord(patronId, bookId, loanDays);
            if (loanId <= 0) {
                throw new DatabaseOperationException("Failed to create loan record");
            }

            loanRepository.setLoanStatus(loanId, "ACTIVE");

            bookRepository.updateBookAvailability(bookId, -1);
            return loanId;
        } catch (Exception e) {
            throw new DatabaseOperationException("Error processing book loan", e);
        }
    }
}