

package services

import (
	"database/sql"
	"fmt"
	"log"
	"sort"
)

type BookRecommendationService struct {
	patronID int
	db       *sql.DB
}

func NewBookRecommendationService(patronID int, db *sql.DB) *BookRecommendationService {
	return &BookRecommendationService{patronID, db}
}

func (s *BookRecommendationService) generateBookRecommendations() ([]map[string]interface{}, error) {
	// Retrieve patron's reading history and preferences
	readingHistory, err := s.getPatronReadingHistory()
	if err != nil {
		return nil, err
	}

	preferences, err := s.getPatronPreferences()
	if err != nil {
		return nil, err
	}

	// Retrieve patron's ratings for each book category and author
	ratings, err := s.getPatronRatings()
	if err != nil {
		return nil, err
	}

	// Retrieve similar patrons who have borrowed the same books as the input patron
	similarPatrons, err := s.getSimilarPatrons()
	if err != nil {
		return nil, err
	}

	// Calculate a score for each book based on the patron's reading history, preferences, and similar patrons' loans
	bookScores := make(map[int]float64)
	for _, book := range readingHistory {
		bookScores[book.ID] = 0
	}

	for _, preference := range preferences {
		for _, book := range readingHistory {
			if book.Category == preference.Category {
				bookScores[book.ID] += preference.Score
			}
		}
	}

	for _, rating := range ratings {
		for _, book := range readingHistory {
			if book.Author == rating.Author {
				bookScores[book.ID] += rating.Score
			}
		}
	}

	for _, patron := range similarPatrons {
		for _, book := range patron.Loans {
			if _, ok := bookScores[book.ID]; ok {
				bookScores[book.ID] += 1
			}
		}
	}

	// Limit the results to the top 10 books with the highest scores
	var recommendedBooks []map[string]interface{}
	for bookID, score := range bookScores {
		recommendedBooks = append(recommendedBooks, map[string]interface{}{
			"book_id": bookID,
			"title":   getBookTitle(bookID, s.db),
			"score":  score,
		})
	}

	sort.Slice(recommendedBooks, func(i, j int) bool {
		return recommendedBooks[i]["score"].(float64) > recommendedBooks[j]["score"].(float64)
	})

	return recommendedBooks[:10], nil
}

func (s *BookRecommendationService) getPatronReadingHistory() ([]Book, error) {
	rows, err := s.db.Query("SELECT * FROM reading_history WHERE patron_id = $1", s.patronID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var readingHistory []Book
	for rows.Next() {
		var book Book
		err := rows.Scan(&book.ID, &book.Title, &book.Category, &book.Author)
		if err != nil {
			return nil, err
		}
		readingHistory = append(readingHistory, book)
	}

	return readingHistory, nil
}

func (s *BookRecommendationService) getPatronPreferences() ([]Preference, error) {
	rows, err := s.db.Query("SELECT * FROM preferences WHERE patron_id = $1", s.patronID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var preferences []Preference
	for rows.Next() {
		var preference Preference
		err := rows.Scan(&preference.ID, &preference.Category, &preference.Score)
		if err != nil {
			return nil, err
		}
		preferences = append(preferences, preference)
	}

	return preferences, nil
}

func (s *BookRecommendationService) getPatronRatings() ([]Rating, error) {
	rows, err := s.db.Query("SELECT * FROM ratings WHERE patron_id = $1", s.patronID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var ratings []Rating
	for rows.Next() {
		var rating Rating
		err := rows.Scan(&rating.ID, &rating.Author, &rating.Score)
		if err != nil {
			return nil, err
		}
		ratings = append(ratings, rating)
	}

	return ratings, nil
}

func (s *BookRecommendationService) getSimilarPatrons() ([]Patron, error) {
	rows, err := s.db.Query("SELECT * FROM patrons WHERE id IN (SELECT patron_id FROM loans WHERE book_id IN (SELECT book_id FROM reading_history WHERE patron_id = $1))", s.patronID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var similarPatrons []Patron
	for rows.Next() {
		var patron Patron
		err := rows.Scan(&patron.ID, &patron.Name)
		if err != nil {
			return nil, err
		}

		patron.Loans, err = s.getPatronLoans(patron.ID)
		if err != nil {
			return nil, err
		}

		similarPatrons = append(similarPatrons, patron)
	}

	return similarPatrons, nil
}

func (s *BookRecommendationService) getPatronLoans(patronID int) ([]Book, error) {
	rows, err := s.db.Query("SELECT * FROM loans WHERE patron_id = $1", patronID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var loans []Book
	for rows.Next() {
		var book Book
		err := rows.Scan(&book.ID, &book.Title, &book.Category, &book.Author)
		if err != nil {
			return nil, err
		}
		loans = append(loans, book)
	}

	return loans, nil
}

func getBookTitle(bookID int, db *sql.DB) string {
	var title string
	err := db.QueryRow("SELECT title FROM books WHERE id = $1", bookID).Scan(&title)
	if err != nil {
		log.Println(err)
		return ""
	}
	return title
}

type Book struct {
	ID       int
	Title    string
	Category string
	Author   string
}

type Preference struct {
	ID       int
	Category string
	Score    float64
}

type Rating struct {
	ID     int
	Author string
	Score  float64
}

type Patron struct {
	ID   int
	Name string
	Loans []Book
}