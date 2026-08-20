import pymupdf
import os
from llama_index.core import Document


def extract_pages_as_document(pdf_path, page_indices, source_name, description, header):
    doc = pymupdf.open(pdf_path)
    combined_text = header + "\n\n"
    for idx in page_indices:
        combined_text += f"--- Page {idx+1} ---\n"
        combined_text += doc[idx].get_text()
        combined_text += "\n\n"
    return Document(
        text=combined_text,
        metadata={
            "source": source_name,
            "type": "table",
            "description": description
        }
    )


def get_table_documents(pdf_dir):
    docs = []

    # 1. HOSTEL FEE TABLE
    docs.append(extract_pages_as_document(
        pdf_path=os.path.join(pdf_dir, "TUITION FEE AND OTHER DUES.pdf"),
        page_indices=[2],
        source_name="TUITION FEE AND OTHER DUES",
        description="Hostel fee table for all hostels on Patiala campus",
        header="HOSTEL FEE TABLE - COMPLETE FEE STRUCTURE FOR ALL HOSTELS PATIALA CAMPUS. Contains per-semester hostel fees for Hostel-A B C E G H I J K L M N O PG Q D FRG FRF. Mess fee for Patiala campus is Rs 26900 per semester."
    ))

    # 2. PROGRAMME FEE TABLE (Indian / other than FN-NRI students)
    docs.append(extract_pages_as_document(
        pdf_path=os.path.join(pdf_dir, "TUITION FEE AND OTHER DUES.pdf"),
        page_indices=[0],
        source_name="TUITION FEE AND OTHER DUES",
        description="Programme fee table for all UG PG PhD programmes",
        header="PROGRAMME FEE TABLE TUITION FEE FOR ALL PROGRAMMES 2026-27. Contains semester-wise fee total programme fee tuition fee development fee and other charges for BE BTech MCA MSc ME MTech MA PhD programmes. Students with PCM score above 80 percent get 30 percent tuition fee waiver. Students with PCM above 75 percent get 20 percent waiver."
    ))

    # 2B. PROGRAMME FEE TABLE - FN/NRI CATEGORY
    docs.append(extract_pages_as_document(
        pdf_path=os.path.join(pdf_dir, "TUITION FEE AND OTHER DUES.pdf"),
        page_indices=[1],
        source_name="TUITION FEE AND OTHER DUES",
        description="Programme fee table in USD for FN/NRI students",
        header="PROGRAMME FEE TABLE FOR FN NRI FOREIGN NATIONAL NRI CATEGORY STUDENTS 2026-27. Fees quoted in USD. Admission fee USD 500. Contains annual programme fee tuition fee development fee and other charges in USD for BE BTech MCA MA MSc ME MTech PhD programmes for FN NRI students."
    ))

    # 2C. HOSTEL FEE TABLE - LMTSM DERA BASSI CAMPUS
    docs.append(extract_pages_as_document(
        pdf_path=os.path.join(pdf_dir, "TUITION FEE AND OTHER DUES.pdf"),
        page_indices=[3],
        source_name="TUITION FEE AND OTHER DUES",
        description="Hostel fee table for LMTSM Dera Bassi campus",
        header="HOSTEL FEE TABLE LMTSM DERA BASSI CAMPUS. Contains per-semester hostel fees for shared non-AC and AC 2 seater and 3 seater rooms at the Dera Bassi campus. Mess fee for Dera Bassi campus is Rs 26300 per semester."
    ))

    # 3. SEAT MATRIX TABLES
    docs.append(extract_pages_as_document(
        pdf_path=os.path.join(pdf_dir, "ADMISSION TO FIRST YEAR UG PROGRAM.pdf"),
        page_indices=[7, 8],
        source_name="ADMISSION TO FIRST YEAR UG PROGRAM",
        description="Seat matrix showing total seats per branch under each category",
        header="SEAT MATRIX SEATS UNDER DIFFERENT CATEGORIES FOR EACH DISCIPLINE. Table IIA total seats per branch. Outside Punjab: SCO STO PHO GENO. Punjab: SCST BC SP PHP GENP. Total intake 3390 seats. Table IIB nomination seats FN NRI CTUE PMSSS GoI JKS LUTS NES."
    ))

    # 4. SCHOLARSHIP POLICY
    docs.append(extract_pages_as_document(
        pdf_path=os.path.join(pdf_dir, "SCHOLARSHIP POLICY.pdf"),
        page_indices=list(range(13)),
        source_name="SCHOLARSHIP POLICY",
        description="Complete scholarship policy with all scholarships eligibility and amounts",
        header="SCHOLARSHIP POLICY COMPLETE LIST OF ALL SCHOLARSHIPS AT TIET 2026-27. Contains merit scholarships need-based government and private scholarships. Includes eligibility criteria annual amounts number of scholarships and conditions."
    ))

    # 5. BRANCH WISE SEAT COUNTS - plain language
    docs.append(Document(
        text="BRANCH WISE SEAT DISTRIBUTION BE BTech PROGRAMS AT TIET 2026-27. Computer Engineering COE 960 seats. Computer Science Engineering Patiala COPC 540 seats. Computer Science Business Systems COBS 60 seats. Artificial Intelligence Data Science DSAI 240 seats. Electronics Communication Engineering ECE 240 seats. Electronics Computer Engineering ENC 360 seats. Electronics Engineering VLSI EVD 90 seats. Electronics Instrumentation Control EIC 90 seats. Electrical Engineering ELE 90 seats. Electrical Computer Engineering EEC 120 seats. Robotics Artificial Intelligence RAI 120 seats. Mechanical Engineering MEE 120 seats. Mechatronics MEC 60 seats. Biotechnology BT 90 seats. Biomedical Engineering BME 30 seats. Chemical Engineering CHE 60 seats. Civil Engineering CIE 90 seats. Civil Engineering Computer Applications CCA 30 seats. Total intake 3390 seats.",
        metadata={
            "source": "ADMISSION TO FIRST YEAR UG PROGRAM",
            "type": "seat_summary",
            "description": "Branch wise seat counts for all BE BTech programs"
        }
    ))

    # 6. FN/NRI AND NOMINATION SEATS - plain language
    docs.append(Document(
        text="FN NRI AND NOMINATION SEATS PER BRANCH TIET 2026-27. ECE has 36 FN NRI seats. COE has 144 FN NRI seats. COPC has 81 FN NRI seats. DSAI has 36 FN NRI seats. ENC has 54 FN NRI seats. BT has 14 FN NRI seats. CHE has 9 FN NRI seats. CIE has 14 FN NRI seats. CCA has 5 FN NRI seats. COBS has 9 FN NRI seats. EIC has 14 FN NRI seats. ELE has 14 FN NRI seats. EEC has 18 FN NRI seats. EVD has 14 FN NRI seats. MEC has 9 FN NRI seats. MEE has 18 FN NRI seats. RAI has 18 FN NRI seats. BME has 5 FN NRI seats. Total FN NRI seats 512. Total CTUE seats 34.",
        metadata={
            "source": "ADMISSION TO FIRST YEAR UG PROGRAM",
            "type": "nomination_seats",
            "description": "FN NRI and nomination seats per branch"
        }
    ))

    # 7. GIRLS SCHOLARSHIP SUMMARY
    docs.append(Document(
        text="""SCHOLARSHIPS AVAILABLE FOR GIRL STUDENTS AT TIET 2026-27

The following scholarships are specifically available for or give preference to girl students:

1. Vimlasons Charitable Foundation Scholarship
   Amount: Rs 50,000 per annum
   Eligibility: One scholarship per year for a girl student in 1st year UG program.

2. AICTE PRAGATI Scholarship for Girl Students
   Amount: Rs 50,000 per annum
   Eligibility: Girl students pursuing technical courses. Applied through AICTE portal.

3. Merit-Cum-Means Scholarship
   Amount: Varies
   Eligibility: Family income less than Rs 10 lakh, CGPA above 7.50, no backlog.
   Note: In case of tie in family income, girl students from families with no male child get preference.

4. Merit-Cum-Means Scholarship Lateral Entry
   Amount: Varies
   Eligibility: Aggregate marks above 70 percent at diploma level, family income less than Rs 10 lakh.
   Note: Girl students from families with no male child get preference in case of tie.

5. General Merit Scholarships Merit Scholarship I through VI
   Available to all eligible students including girls based on PCM aggregate percentage at 10+2 level.
   Top performers get tuition fee and development fee waiver.

For government scholarships students must first register on the National Scholarship Portal NSP at scholarships.gov.in.""",
        metadata={
            "source": "SCHOLARSHIP POLICY",
            "type": "girls_scholarship_summary",
            "description": "Scholarships available for girl students at TIET"
        }
    ))

    # 8. GIRLS HOSTEL SUMMARY
    docs.append(Document(
        text="""GIRLS HOSTEL OPTIONS AT TIET PATIALA - FIRST YEAR UG STUDENTS

The Institute has 7 hostels for girls. For first-year UG girl students the following hostels are available (tentative):

1. Vasudha Hall previously known as Hostel E
   Room Type: Three Seater or Four Seater AC
   Total Seats: 180

2. Vasudha Hall previously known as Hostel G
   Room Type: Three Seater or Four Seater AC
   Total Seats: 180

3. Ira Hall previously known as Hostel I
   Room Type: One Seater Non-AC or Three Seater AC
   Total Seats: 320

4. Vani PG II Hostel
   Room Type: Two Seater AC
   Total Seats: 400

Total first-year seats for girl students: approximately 1080 seats.
All girl hostels are managed under the Dean Students Office.
Students within 50km of the institute are not eligible for hostel accommodation.
Mess subscription is mandatory for all hostel residents.
NRI and Foreign students may reserve rooms in advance.""",
        metadata={
            "source": "25 HOSTEL FACILITIES",
            "type": "girls_hostel_summary",
            "description": "Girls hostel options and seat counts for first year UG students"
        }
    ))

    # 9. BOYS HOSTEL SUMMARY (with per-semester fee, resolved via hall-name-to-code mapping)
    docs.append(Document(
        text="""BOYS HOSTEL OPTIONS AND FEES AT TIET PATIALA - FIRST YEAR UG STUDENTS

The Institute has 10 hostels for boys. For first-year UG boy students the following hostels
are available (tentative), with per-semester hostel fee (Patiala campus):

1. Ambaram Hall (previously known as Hostel-K)
   Room Type: Two Seater Non-AC or Two Seater AC
   Total Seats: 600
   Fee: Rs 45,500/semester (Non-AC), Rs 57,000/semester (AC)

2. Viyat Hall (previously known as Hostel-L)
   Room Type: Two Seater AC
   Total Seats: 200
   Fee: Rs 57,000/semester (AC)

3. Tejas Hall (previously known as Hostel-J)
   Room Type: One Seater Non-AC or Two Seater AC
   Total Seats: 950
   Fee: Rs 51,000/semester (1-seater Non-AC), Rs 57,000/semester (2-seater AC)

4. Vyan Hall (previously known as Hostel-H)
   Room Type: Four Seater AC, with and without bunk beds
   Total Seats: 670
   Fee: Rs 45,600/semester (4-seater AC)

Mess Fee: Rs 26,900/- per semester for Patiala Campus (same for all hostels, mandatory).

Total first-year seats for boy students: approximately 2420 seats.
Accommodation for all students (UG/PG/PhD) is subject to availability and allotted on merit basis.
Students within 50km of the institute are not eligible for hostel accommodation.
NRI and Foreign students may reserve rooms in advance.""",
        metadata={
            "source": "25 HOSTEL FACILITIES",
            "type": "boys_hostel_summary",
            "description": "Boys hostel options, seat counts and fees for first year UG students"
        }
    ))

    # 9C. HOSTEL HALL NAME TO OLD CODE MAPPING (all 10 boys' halls, for later-year queries)
    docs.append(Document(
        text="""TIET HOSTEL HALL NAMES - MAPPING TO OLD HOSTEL CODES (BOYS HOSTELS)

The 10 boys' hostels at TIET Patiala were renamed from their old letter codes. Current name
(previous code), useful for looking up per-semester fees in the hostel fee table:

- Agira Hall (previously Hostel-A)
- Amritam Hall (previously Hostel-B)
- Prithvi Hall (previously Hostel-C)
- Neeram Hall (previously Hostel-D)
- Vyan Hall (previously Hostel-H)
- Tejas Hall (previously Hostel-J)
- Ambaram Hall (previously Hostel-K)
- Viyat Hall (previously Hostel-L)
- Anantam Hall (previously Hostel-M)
- Vyom Hall (previously Hostel-O)

Only Ambaram Hall, Viyat Hall, Tejas Hall and Vyan Hall are designated for first-year UG boy
students (tentative allocation). Agira, Amritam, Prithvi, Neeram, Anantam and Vyom Halls
house students from later years.""",
        metadata={
            "source": "25 HOSTEL FACILITIES",
            "type": "boys_hostel_name_mapping",
            "description": "Mapping of current boys hostel hall names to old hostel letter codes"
        }
    ))

    # 9B. HOSTEL RULES, TIMINGS AND DISCIPLINE
    docs.append(Document(
        text="""HOSTEL TIMINGS, CURFEW AND DISCIPLINE RULES AT TIET PATIALA

Entry/gate timing (curfew): The main gate entry timing is restricted to 8:00 PM. Hostel in-time
(the time by which every hostel resident must be back inside their hostel) is 8:30 PM, across
all hostels (both boys and girls). It is mandatory for every hostel resident to mark their
attendance daily with the night caretaker; a student attendance record is maintained in
each hostel.

No student should stay away from their room during the night except in exceptional cases
with prior written permission of the warden.

Other hostel discipline rules:
- No powered vehicles (bikes, cars, scooters) are allowed on campus for hostellers; only
  bicycles are permitted.
- Smoking and drinking are strictly prohibited in the hostels and on the campus.
- Anti-ragging and anti-drug-abuse policies are strictly enforced.
- Pets of all kinds are prohibited inside the hostels; feeding stray animals in hostel premises
  is not permitted.
- No male visitors are allowed to visit girl students in the hostel premises.
- Parents must submit the name of a local guardian for their ward.
- Students are advised not to keep large cash or valuables in their hostel room; the Institute
  is not responsible for any loss of belongings.
- Loud music, partying, singing, shouting, or any noise that disturbs other hostellers is not
  allowed.
- Subscription to the hostel mess is mandatory for every hostel resident; opting out of mess
  is not permitted under any circumstances.
- Laundry service is provided free of charge to all hostel residents (a laundry card must be
  issued).
- Damage to hostel property invites severe disciplinary action, including possible expulsion
  from the hostel.""",
        metadata={
            "source": "25 HOSTEL FACILITIES",
            "type": "hostel_rules_timings",
            "description": "Hostel entry timings, curfew, attendance, and discipline rules"
        }
    ))

    # 10. REFUND POLICY
    docs.append(extract_pages_as_document(
        pdf_path=os.path.join(pdf_dir, "Admissions 2026-2027 Refund Policy.pdf"),
        page_indices=[0],
        source_name="Admissions 2026-2027 Refund Policy",
        description="Refund policy for academic fee and hostel/mess fee on withdrawal",
        header="ADMISSIONS 2026-2027 REFUND POLICY. Academic fee refund: full refund minus Rs 1000 if withdrawn on or before July 20 2026, no refund after that date. Hostel and mess fee refund: 75 percent refund if vacated within 4 weeks of start of classes, 50 percent refund if vacated after 4 weeks but within 8 weeks, no refund after 8 weeks of start of classes."
    ))

    return docs