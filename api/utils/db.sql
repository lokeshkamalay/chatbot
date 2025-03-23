-- Create Table
CREATE TABLE ai.tbl_chat_history (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(255) NOT NULL,  -- Unique session identifier
    username VARCHAR(255) NOT NULL,  -- User identifier (could be user ID or name)
    rolename VARCHAR(50) CHECK (rolename IN ('user', 'assistant', 'system', 'bot')),  -- Role in chat
    message TEXT NOT NULL,  -- ChatGPT response or user message
    created_at TIMESTAMPTZ DEFAULT NOW(),  -- Timestamp of the message
    message_tokens INT DEFAULT 0,  -- Token count for cost analysis
    total_tokens INT DEFAULT 0,  -- Running total per session
    parent_message_id INT,  -- For threaded conversations (optional)
    FOREIGN KEY (parent_message_id) REFERENCES ai.tbl_chat_history(id) ON DELETE SET NULL
);
-- Indexes for better query performance
CREATE INDEX idx_session_id ON ai.tbl_chat_history(session_id);
CREATE INDEX idx_user ON ai.tbl_chat_history(username);
CREATE INDEX idx_created_at ON ai.tbl_chat_history(created_at);
-- Add a unique constraint to prevent duplicate messages in the same session
ALTER TABLE ai.tbl_chat_history ADD CONSTRAINT unique_message_per_session UNIQUE (session_id, message, created_at);


---------------------------
-- Create fule table
create table ai.tbl_documents (
	id 	SERIAL PRIMARY KEY,
	filename varchar(250) NOT NULL,
	inserted_by varchar(100) DEFAULT 'Auto',
	created_at TIMESTAMPTZ DEFAULT NOW()
)
