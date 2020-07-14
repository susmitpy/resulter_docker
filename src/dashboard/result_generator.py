from management.models import Student, Assessment

import pandas as pd
from numpy import where as np_where
from numpy import ceil
from numpy import round
from numpy import zeros

from django.db.models import Max

from jinja2 import Environment, FileSystemLoader
from django.core.files.storage import default_storage

import tempfile

def apply_grace_marks(df,ld=False,sports=False,sports_marks=0):

    if df["%"].min() < 25:
        return {"status":"FAIL",
                "df":df,
                "ld":ld,
                "sports":sports,
                "sports_remain_marks":sports_marks
                }

    df["Grace Marks"]= zeros((len(df),1),dtype=int)

    fail = df[df["%"] < 35].sort_values("%",ascending=False)
    perc_index = df.columns.get_loc("%")
    gm_index= df.columns.get_loc("Grace Marks")
    len_fail = len(fail)

    if len_fail == 0:
        return {"status":"PASS",
                "df":df,
                "ld":ld,
                "sports":sports,
                "sports_remain_marks":sports_marks
                }

    # Required Grace Marks for Passing
    for i in range(len_fail):

        fail.iloc[i,gm_index] = 35 - fail.iloc[i,perc_index]

    if sports:
        # apply sports marks in grace
        # first to subjects with highest marks

         for i in range(len_fail):
            if sports_marks == 0:
                break
            if fail.iloc[i,gm_index] <= sports_marks:
                sports_marks -= fail.iloc[i,gm_index]
                fail.iloc[i,gm_index] = 0

            else:
                grace_needed = fail.iloc[i,gm_index]-sports_marks
                sports_marks = 0
                fail.iloc[i,gm_index] = grace_needed

         df.loc[list(fail.index)] = fail


    if ld:
        # check by ld constraints
        # first to subjects with highest marks
        if fail["Grace Marks"].sum() > 20:
            return {"status":"FAIL",
                    "df":df,
                    "ld":ld,
                    "sports":sports,
                    "sports_remain_marks":sports_marks
                    }


        # Within Constraints so PASS
        return     {"status":"PASS",
                    "df":df,
                    "ld":ld,
                    "sports":sports,
                    "sports_remain_marks":sports_marks
                    }

    # Normal Grace Marks Constraints
    if fail["Grace Marks"].sum() > 15:
        return {"status":"FAIL",
                "df":df,
                "ld":ld,
                "sports":sports,
                "sports_remain_marks":sports_marks
                }

    still_failing_in_n_subjects = sum(fail["Grace Marks"]>0)
    if still_failing_in_n_subjects > 3:
        return {"status":"FAIL",
                "df":df,
                "ld":ld,
                "sports":sports,
                "sports_remain_marks":sports_marks
                }

    df.loc[list(fail.index)] = fail
    return {"status":"PASS",
                "df":df,
                "ld":ld,
                "sports":sports,
                "sports_remain_marks":sports_marks
                }

def get_marks(x):
	if type(x) == int:
		return x
	return 0

def get_sub_total(row):
     unit_one_marks = get_marks(row["Unit 1"])
     term_marks = get_marks(row["Terminal"])
     unit_two_marks = get_marks(row["Unit 2"])
     final_marks = row["Final"]
     splitted = final_marks.split(" + ")
     theory = get_marks(int(splitted[0]))
     oral = get_marks(int(splitted[1]))
     return unit_one_marks + term_marks + unit_two_marks + theory + oral

def color_cell(cell):
    try:
        a = int(cell)
        return ""
    except ValueError:
        if "+" in cell:
            return ""

        return "background-color: #f7e06a"

def color_sub_perc(cell):
    if cell < 35:
        return "color: #f20c0c"
    return ""

# DB CHECK PASS
def generate_intermediate_result(division):
    students = Student.objects.filter(division=division).exclude(vacant = False)
    results = []
    for index, student in enumerate(students):
        ass = Assessment.objects.filter(student=student).values("exam__name","exam__subject__name","marks","note")
        df = pd.DataFrame(ass)
        df.columns=["exam","subject","marks","note"]
        df["note"] = df["note"].replace({"ABSENT":"AB","BLANK":"BLK"})
        df["marks"] = np_where(df["marks"]==-1,df["note"],df["marks"])
        df=df.drop(["note"],axis=1)

        theory = df[df["exam"]=="final_theory"].drop("exam",axis=1)
        oral = df[df["exam"]=="final_oral"].drop("exam",axis=1)
        final=theory.merge(oral,on="subject",suffixes=["_theory","_oral"])
        final["marks"] = final["marks_theory"].map(str) + " + " + final["marks_oral"].map(str)
        final = final.drop(["marks_theory","marks_oral"],axis=1)
        final["exam"]="final"

        # Remove final_theory, final_oral
        df=df.drop(df[df["exam"].str.startswith("final")].index)
        ready_for_tabulation = pd.concat([df,final])

        data = []
        for s in ready_for_tabulation["subject"].unique():
                  row = [s]
                  sub_data = ready_for_tabulation[ready_for_tabulation["subject"]==s]
                  for e in ["unit_one","terminal","unit_two","final"]:
                     row.append(sub_data[sub_data["exam"]==e].marks.values[0])
                  data.append(row)
        df=pd.DataFrame(data,columns=["Subject","Unit 1","Terminal","Unit 2","Final"]).set_index("Subject")

        df["Total"] = df.apply(get_sub_total,axis=1)
        df["%"] = ceil(df["Total"] / 2)
        df["%"] = df["%"].round(2)

        ld = student.identifier == "LD"
        sports = student.sports > 0
        if sports:
            sports_marks = s.sportsdata_set.aggregate(Max("extra_marks")).get("extra_marks__max")
        else:
            sports_marks = 0

        result = apply_grace_marks(df,ld=ld,sports=sports,sports_marks=sports_marks)

        df = result["df"]
        status = result["status"]
        sports_remain_marks = result["sports_remain_marks"]

        if status == "FAIL":
            df.drop("Grace Marks",axis=1,inplace=True)
        else:
            uni = df["Grace Marks"].unique()
            if len(uni) == 1 and uni[0] == 0:
                df.drop("Grace Marks",axis=1,inplace=True)


        df.index.name=None
        total_marks = int(ceil(df.Total / 2).sum())
        if sports:
            marks = " ".join([str(total_marks),"+",str(sports_remain_marks)])
            final_perc = round((total_marks + sports_remain_marks)/len(df),2)
        else:
            marks = total_marks
            final_perc = round(total_marks/len(df),2)

        non_int_color_cols = ["Unit 1","Terminal","Unit 2","Final"]
        html =df.style.applymap(color_cell,subset=non_int_color_cols).applymap(color_sub_perc,subset=["%"]).set_table_attributes("class='dataframe mystyle'").set_precision(2).render()

        env = Environment(loader=FileSystemLoader('./result'))
        template = env.get_template("student_result.html")
        template_vars = {"title" : "Result",
                         "name" : student.name,
                         "roll" : student.roll_num,
                         "division" : division,
                         "marks": marks,
                         "final_perc" : final_perc,
                         "result":html,
                         "status":status,
                         "sports_remain_marks":sports_remain_marks,
                         "sports" : sports,
                         "ld" : ld
                        }

        html_out = template.render(template_vars)
        fp = "./student_results/{}/roll_{}.html".format(division,str(student.roll_num))
        default_storage.delete(fp)
        f = tempfile.TemporaryFile(mode="w+")
        f.write(html_out)
        default_storage.save(fp, f)

        result_map = {
            "id" : index,
            "name" : student.name,
            "roll" : student.roll_num,
            "division" : division,
            "marks": marks,
            "final_perc" : final_perc,
            "result":html,
            "status":status,
            "sports_remain_marks":sports_remain_marks,
            "sports" : sports,
            "ld" : ld
        }

        results.append(result_map)

    env = Environment(loader=FileSystemLoader('./result'))
    template = env.get_template("inter_result.html")
    template_vars = {"title" : "College Result",
                     "division" : division,
                     "results":results
                    }
    html_out = template.render(template_vars)
    file_path = "./results/intermediate_result.html"
    default_storage.delete(file_path)
    f = tempfile.TemporaryFile(mode="w+")
    f.write(html_out)

    file_name = default_storage.save(file_path, f)
    return file_path
