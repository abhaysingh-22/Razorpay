export interface Transaction {
  id: string;
  razorpay_payment_id: string | null;
  amount: number;
  currency: string;
  status: string;
  failure_reason: string;
  customer_id: string;
  next_retry_at: string | null;
  created_at: string;
}

export interface RecoveryAttempt {
  id: string;
  transaction_id: string;
  attempt_number: number;
  action_taken: string;
  reasoning: string | null;
  outcome: string | null;
  amount_recovered: number;
  created_at: string;
}

export interface BatchSummary {
  id: string;
  total_transactions: number;
  total_amount_at_risk: number;
  total_amount_recovered: number;
  recovery_rate: number;
  breakdown_by_reason: Record<string, { count: number; recovered: number }>;
  key_highlights: string[];
  exceptions: string[];
  created_at: string;
}