

package src.models;

import java.time.LocalDateTime;

public class AuditLog {
    private String tableName;
    private int recordId;
    private String actionType;
    private LocalDateTime actionTimestamp;
    private String newValues;

    public AuditLog(String tableName, int recordId, String actionType, LocalDateTime actionTimestamp, String newValues) {
        if (tableName == null || tableName.isEmpty()) {
            throw new IllegalArgumentException("Table name cannot be null or empty");
        }
        if (recordId < 0) {
            throw new IllegalArgumentException("Record id cannot be negative");
        }
        if (actionType == null || actionType.isEmpty()) {
            throw new IllegalArgumentException("Action type cannot be null or empty");
        }
        if (actionTimestamp == null) {
            throw new IllegalArgumentException("Action timestamp cannot be null");
        }
        if (newValues == null || newValues.isEmpty()) {
            throw new IllegalArgumentException("New values cannot be null or empty");
        }
        this.tableName = tableName;
        this.recordId = recordId;
        this.actionType = actionType;
        this.actionTimestamp = actionTimestamp;
        this.newValues = newValues;
    }

    public String getTableName() {
        return tableName;
    }

    public void setTableName(String tableName) {
        if (tableName == null || tableName.isEmpty()) {
            throw new IllegalArgumentException("Table name cannot be null or empty");
        }
        this.tableName = tableName;
    }

    public int getRecordId() {
        return recordId;
    }

    public void setRecordId(int recordId) {
        if (recordId < 0) {
            throw new IllegalArgumentException("Record id cannot be negative");
        }
        this.recordId = recordId;
    }

    public String getActionType() {
        return actionType;
    }

    public void setActionType(String actionType) {
        if (actionType == null || actionType.isEmpty()) {
            throw new IllegalArgumentException("Action type cannot be null or empty");
        }
        this.actionType = actionType;
    }

    public LocalDateTime getActionTimestamp() {
        return actionTimestamp;
    }

    public void setActionTimestamp(LocalDateTime actionTimestamp) {
        if (actionTimestamp == null) {
            throw new IllegalArgumentException("Action timestamp cannot be null");
        }
        this.actionTimestamp = actionTimestamp;
    }

    public String getNewValues() {
        return newValues;
    }

    public void setNewValues(String newValues) {
        if (newValues == null || newValues.isEmpty()) {
            throw new IllegalArgumentException("New values cannot be null or empty");
        }
        this.newValues = newValues;
    }
}