import api from "./client";
import { Transaction, RecoveryAttempt, BatchSummary } from "../types";

export const getTransactions = async (status?: string) => {
  const res = await api.get<Transaction[]>("/transactions/", { params: { status } });
  return res.data;
};

export const getTransactionDetail = async (id: string) => {
  const res = await api.get(`/transactions/${id}`);
  return res.data as { transaction: Transaction; recovery_attempts: RecoveryAttempt[] };
};

export const injectPayments = async (count: number = 10) => {
  const res = await api.post(`/transactions/generate?count=${count}`);
  return res.data as { status: string; inserted: number; transactions: Transaction[] };
};

export const getLatestSummary = async () => {
  const res = await api.get<BatchSummary>("/metrics/summary");
  return res.data;
};

export const getSummaryHistory = async () => {
  const res = await api.get<BatchSummary[]>("/metrics/history");
  return res.data;
};

export const runRecoveryBatch = async () => {
  const res = await api.post("/recovery/run");
  return res.data;
};

export const getRecoveryAttempts = async () => {
  const res = await api.get<RecoveryAttempt[]>("/recovery/attempts");
  return res.data;
};

export const getReviewQueue = async () => {
  const res = await api.get<Transaction[]>("/recovery/review-queue");
  return res.data;
};

export const resolveReview = async (transactionId: string, decision: "approve" | "reject", notes?: string) => {
  const res = await api.post(`/recovery/review-queue/${transactionId}/resolve`, { decision, notes });
  return res.data;
};