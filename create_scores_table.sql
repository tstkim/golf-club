-- Supabase에서 실행할 SQL
-- scores 테이블 생성

CREATE TABLE IF NOT EXISTS scores (
    id BIGSERIAL PRIMARY KEY,
    game_date DATE NOT NULL,
    member_id BIGINT REFERENCES members(id) ON DELETE SET NULL,
    member_name TEXT NOT NULL,
    grade CHAR(1) NOT NULL CHECK (grade IN ('A', 'B', 'C')),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 인덱스 생성 (조회 성능 향상)
CREATE INDEX IF NOT EXISTS idx_scores_game_date ON scores(game_date);
CREATE INDEX IF NOT EXISTS idx_scores_grade ON scores(grade);

-- RLS 비활성화 (service_role 키 사용 시)
ALTER TABLE scores ENABLE ROW LEVEL SECURITY;

-- 모든 작업 허용 정책
CREATE POLICY "Allow all operations" ON scores
    FOR ALL
    USING (true)
    WITH CHECK (true);
