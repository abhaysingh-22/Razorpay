create table transactions (
    id uuid primary key default gen_random_uuid(),
    razorpay_payment_id text,
    amount numeric not null,
    currency text default 'INR',
    status text not null,              -- 'failed', 'recovered', 'exhausted'
    failure_reason text,               -- 'insufficient_funds', 'expired_card', 'bank_timeout', 'fraud_flag'
    customer_id text,
    created_at timestamptz default now()
);

create table recovery_attempts (
    id uuid primary key default gen_random_uuid(),
    transaction_id uuid references transactions(id),
    attempt_number int not null,
    action_taken text not null,        -- 'retry_scheduled', 'card_update_requested', 'escalated', 'stopped'
    reasoning text,                    -- LLM's explanation, your audit trail
    outcome text,                      -- 'success', 'failed', 'pending'
    amount_recovered numeric default 0,
    next_retry_at timestamptz,
    created_at timestamptz default now()
);

create table batch_summaries (
    id uuid primary key default gen_random_uuid(),
    total_transactions int not null,
    total_amount_at_risk numeric not null,
    total_amount_recovered numeric not null,
    recovery_rate numeric not null,           -- percentage
    breakdown_by_reason jsonb not null,        -- {"insufficient_funds": {"count": 30, "recovered": 22}, ...}
    key_highlights text[] not null,            -- plain-English bullet points
    exceptions text[] not null,                -- cases that couldn't be recovered, and why
    created_at timestamptz default now()
);