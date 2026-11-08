// TypeScript mirror of agent/taxonomy.py for the review dashboard.
// Keep values identical to the Python enums.

export const DocumentType = {
  CapitalCall: "capital_call",
  DistributionNotice: "distribution_notice",
  QuarterlyReport: "quarterly_report",
  CapitalAccountStatement: "capital_account_statement",
  ConsentRequest: "consent_request",
  Other: "other",
  Undetermined: "undetermined",
} as const;
export type DocumentType = (typeof DocumentType)[keyof typeof DocumentType];

export const InfoGrade = {
  Public: "public",
  Internal: "internal",
  ContractualConfidential: "contractual_confidential",
  Restricted: "restricted",
} as const;
export type InfoGrade = (typeof InfoGrade)[keyof typeof InfoGrade];

export const ObligationType = {
  Funding: "funding",
  ResponseConsent: "response_consent",
  RightElection: "right_election",
  TaxReclaim: "tax_reclaim",
  ProxyVote: "proxy_vote",
  Undetermined: "undetermined",
} as const;
export type ObligationType = (typeof ObligationType)[keyof typeof ObligationType];

export const AlertType = {
  DataError: "data_error",
  ExplainedMove: "explained_move",
  UnexplainedMove: "unexplained_move",
} as const;
export type AlertType = (typeof AlertType)[keyof typeof AlertType];

/** Evidence location shown to the reviewer so a decision can be checked in seconds. */
export interface Evidence {
  page: number;
  excerpt: string;
}

/** One classified document as stored in Supabase and shown on the review screen. */
export interface ClassifiedDocument {
  id: string;
  fundName: string;
  predictionSet: DocumentType[];
  grade: InfoGrade;
  extracted: Record<string, string | number | null>;
  evidence: Evidence[];
  needsHumanReview: boolean;
  receivedAt: string; // ISO 8601
}

export function needsHumanReview(predictionSet: DocumentType[]): boolean {
  return predictionSet.length !== 1 || predictionSet.includes(DocumentType.Undetermined);
}
