

package app.services

import app.repositories.BookRepository
import app.repositories.LoanRepository
import app.repositories.PatronRepository
import java.lang.IllegalArgumentException
import java.lang.IllegalStateException

class BookLoanService {
    private val bookRepository = BookRepository()
    private val loanRepository = LoanRepository()
    private val patronRepository = PatronRepository()

    fun processBookLoan(patronId: Int, bookId: Int, loanDays: Int) {
        if (loanDays <= 0) {
            throw IllegalArgumentException("Loan days must be a positive integer")
        }

        if (patronId <= 0) {
            throw IllegalArgumentException("Patron ID must be a positive integer")
        }

        if (bookId <= 0) {
            throw IllegalArgumentException("Book ID must be a positive integer")
        }

        try {
            val availableCopies = bookRepository.getAvailableCopies(bookId)
            if (availableCopies <= 0) {
                throw IllegalStateException("Book is not available for loan")
            }

            val (patronStatus, activeLoans) = patronRepository.getPatronStatusAndActiveLoans(patronId)
            if (patronStatus != "ACTIVE" || activeLoans >= 5) {
                throw IllegalStateException("Patron's account is not active or they have reached the maximum number of loans")
            }

            loanRepository.createLoanRecord(patronId, bookId, loanDays)
            bookRepository.updateBookAvailability(bookId, -1)
        } catch (e: Exception) {
            throw IllegalStateException("Failed to process book loan", e)
        }
    }
}