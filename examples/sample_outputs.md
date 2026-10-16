# Sample outputs

> Generated with `python main.py evaluate` after running `python main.py ingest`.
> Answers are grounded in `data/sample_docs/` — note the source citations.

## Q1: How many vacation days do employees get per year?

**DocuChat:** Full-time employees receive 20 vacation days per year, accrued monthly, with up to 5 unused days rolling over to the next year. [company_handbook.md]

**Sources:** company_handbook.md · **Chunks retrieved:** 4

---

## Q2: What is the company's remote work policy?

**DocuChat:** Nimbus Analytics is remote-first — employees may work from anywhere in the United States, but engineers should be online during core collaboration hours (10:00 AM–3:00 PM Central). There is a $1,200 one-time home-office stipend plus $75/month for internet and co-working. [company_handbook.md]

**Sources:** company_handbook.md · **Chunks retrieved:** 4

---

## Q3: What is included in the Pro pricing tier?

**DocuChat:** The Pro tier costs $99/month and includes unlimited dashboards, 10 data sources, 13-month data history, anomaly alerts, Slack integration, and priority email support. [product_faq.md]

**Sources:** product_faq.md · **Chunks retrieved:** 4

---

## Q4: How long is customer data retained after cancellation?

**DocuChat:** After cancellation, customer data is retained for 30 days and then permanently deleted. Enterprise customers can negotiate custom retention terms. [product_faq.md]

**Sources:** product_faq.md · **Chunks retrieved:** 4

---

## Q5: Who is the CEO of Nimbus Analytics?

**DocuChat:** I don't know based on the provided documents.

**Sources:** company_handbook.md, product_faq.md · **Chunks retrieved:** 4

> Q5 demonstrates the groundedness guardrail: when the answer is not in the
> retrieved context, the bot refuses to hallucinate instead of inventing a name.
