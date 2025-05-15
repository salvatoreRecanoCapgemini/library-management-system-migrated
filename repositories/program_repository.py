

package repositories

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

import javax.mail.Message;
import javax.mail.MessagingException;
import javax.mail.Session;
import javax.mail.Transport;
import javax.mail.internet.InternetAddress;
import javax.mail.internet.MimeMessage;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import com.fasterxml.jackson.databind.ObjectMapper;

import repositories.model.AttendanceRecord;
import repositories.model.CompletionStatistics;
import repositories.model.LogEntry;
import repositories.model.ProgramDetails;
import repositories.model.Registration;

public class ProgramRepository {
    private static final Logger logger = LogManager.getLogger(ProgramRepository.class);
    private static final String DB_URL = "jdbc:mysql://localhost:3306/library_programs";
    private static final String DB_USER = "root";
    private static final String DB_PASSWORD = "password";
    private static final String MAIL_SERVER = "smtp.gmail.com";
    private static final String MAIL_PORT = "587";
    private static final String MAIL_USERNAME = "your-email@gmail.com";
    private static final String MAIL_PASSWORD = "your-password";

    public ProgramRepository() {
        try {
            Class.forName("com.mysql.cj.jdbc.Driver");
        } catch (ClassNotFoundException e) {
            logger.error("Error loading MySQL driver", e);
        }
    }

    public ProgramDetails getProgramData(int programId) {
        String query = "SELECT * FROM library_programs WHERE program_id = ?";
        try (Connection conn = DriverManager.getConnection(DB_URL, DB_USER, DB_PASSWORD);
             PreparedStatement stmt = conn.prepareStatement(query)) {
            stmt.setInt(1, programId);
            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    return extractProgramDetails(rs);
                }
            }
        } catch (SQLException e) {
            logger.error("Error retrieving program data", e);
        }
        return null;
    }

    public ProgramDetails extractProgramDetails(ResultSet rs) throws SQLException {
        ProgramDetails programDetails = new ProgramDetails();
        programDetails.setProgramId(rs.getInt("program_id"));
        programDetails.setProgramName(rs.getString("program_name"));
        programDetails.setProgramStatus(rs.getString("program_status"));
        programDetails.setProgramStartDate(rs.getDate("program_start_date"));
        programDetails.setProgramEndDate(rs.getDate("program_end_date"));
        programDetails.setRegistrations(rs.getInt("registrations"));
        programDetails.setCapacity(rs.getInt("capacity"));
        return programDetails;
    }

    public void startProgram(ProgramDetails programDetails) {
        if (!programDetails.getProgramStatus().equals("PUBLISHED")) {
            throw new RuntimeException("Program is not in PUBLISHED status");
        }

        if (programDetails.getRegistrations() < programDetails.getCapacity()) {
            createWaitlistNotificationBatch(programDetails);
            updateProgramStatus(programDetails, "CANCELLED");
            throw new RuntimeException("Program does not have sufficient registrations");
        }

        initializeSessionSchedule(programDetails);
        updateProgramStatus(programDetails, "IN_PROGRESS");
    }

    public void recordAttendance(ProgramDetails programDetails, List<Registration> registrations) {
        if (!programDetails.getProgramStatus().equals("IN_PROGRESS")) {
            throw new RuntimeException("Program is not in IN_PROGRESS status");
        }

        List<AttendanceRecord> attendanceRecords = getAttendanceRecords(programDetails.getProgramId());
        for (Registration registration : registrations) {
            updateAttendanceLog(registration, attendanceRecords);
        }
        for (Registration registration : registrations) {
            generateAttendanceNotification(registration);
        }
    }

    public void completeProgram(ProgramDetails programDetails) {
        if (!programDetails.getProgramStatus().equals("IN_PROGRESS")) {
            throw new RuntimeException("Program is not in IN_PROGRESS status");
        }

        CompletionStatistics completionStatistics = calculateCompletionStatistics(programDetails);
        updateCompletionStatus(programDetails, completionStatistics);
        updateProgramStatus(programDetails, "COMPLETED");
    }

    public void logProgramStateChange(int programId, String action, List<Registration> registrations) {
        LogEntry logEntry = createLogEntry(programId, action, registrations);
        insertLogEntry(logEntry);
    }

    public void manageProgramLifecycle(int programId, String action, List<Registration> registrations) {
        ProgramDetails programDetails = getProgramData(programId);
        if (action.equals("START_PROGRAM")) {
            startProgram(programDetails);
        } else if (action.equals("RECORD_ATTENDANCE")) {
            recordAttendance(programDetails, registrations);
        } else if (action.equals("COMPLETE_PROGRAM")) {
            completeProgram(programDetails);
        } else {
            throw new RuntimeException("Invalid action");
        }
        logProgramStateChange(programId, action, registrations);
    }

    public void createWaitlistNotificationBatch(ProgramDetails programDetails) {
        // Implement createWaitlistNotificationBatch
    }

    public void initializeSessionSchedule(ProgramDetails programDetails) {
        // Implement initializeSessionSchedule
    }

    public void updateProgramStatus(ProgramDetails programDetails, String status) {
        String query = "UPDATE library_programs SET program_status = ? WHERE program_id = ?";
        try (Connection conn = DriverManager.getConnection(DB_URL, DB_USER, DB_PASSWORD);
             PreparedStatement stmt = conn.prepareStatement(query)) {
            stmt.setString(1, status);
            stmt.setInt(2, programDetails.getProgramId());
            stmt.executeUpdate();
        } catch (SQLException e) {
            logger.error("Error updating program status", e);
        }
    }

    public List<AttendanceRecord> getAttendanceRecords(int programId) {
        String query = "SELECT * FROM attendance_records WHERE program_id = ?";
        try (Connection conn = DriverManager.getConnection(DB_URL, DB_USER, DB_PASSWORD);
             PreparedStatement stmt = conn.prepareStatement(query)) {
            stmt.setInt(1, programId);
            try (ResultSet rs = stmt.executeQuery()) {
                List<AttendanceRecord> attendanceRecords = new ArrayList<>();
                while (rs.next()) {
                    AttendanceRecord attendanceRecord = new AttendanceRecord();
                    attendanceRecord.setProgramId(rs.getInt("program_id"));
                    attendanceRecord.setRegistrationId(rs.getInt("registration_id"));
                    attendanceRecord.setAttendanceDate(rs.getDate("attendance_date"));
                    attendanceRecords.add(attendanceRecord);
                }
                return attendanceRecords;
            }
        } catch (SQLException e) {
            logger.error("Error retrieving attendance records", e);
        }
        return null;
    }

    public void updateAttendanceLog(Registration registration, List<AttendanceRecord> attendanceRecords) {
        // Implement updateAttendanceLog
    }

    public void generateAttendanceNotification(Registration registration) {
        // Implement generateAttendanceNotification
        try {
            Session session = Session.getInstance(System.getProperties(), null);
            MimeMessage message = new MimeMessage(session);
            message.setFrom(new InternetAddress(MAIL_USERNAME));
            message.setRecipient(Message.RecipientType.TO, new InternetAddress(registration.getEmail()));
            message.setSubject("Attendance Notification");
            message.setText("You have been marked as attended for the program.");
            Transport transport = session.getTransport("smtp");
            transport.connect(MAIL_SERVER, Integer.parseInt(MAIL_PORT), MAIL_USERNAME, MAIL_PASSWORD);
            transport.sendMessage(message, message.getAllRecipients());
            transport.close();
        } catch (MessagingException e) {
            logger.error("Error sending attendance notification", e);
        }
    }

    public CompletionStatistics calculateCompletionStatistics(ProgramDetails programDetails) {
        // Implement calculateCompletionStatistics
        return null;
    }

    public void updateCompletionStatus(ProgramDetails programDetails, CompletionStatistics completionStatistics) {
        // Implement updateCompletionStatus
    }

    public LogEntry createLogEntry(int programId, String action, List<Registration> registrations) {
        // Implement createLogEntry
        return null;
    }

    public void insertLogEntry(LogEntry logEntry) {
        // Implement insertLogEntry
    }
}