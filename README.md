"# WEB-PROJECT-" 
# WEB-PROJECT
מטרת הפרויקט היא לפתח מערכת מידע קלאסית לניהול תחום הזמנות אוכל. מערכת זו תתמוך בניהול משתמשים והזמנות, תאפשר למנהלים להזין פרטי מנות, למתפעלים לצפות בהזמנות ולסגור אותן, וללקוחות לבצע הזמנות ולהזין חוות דעת. המערכת תשולב עם כלי ניהול זהויות, תספק ממשק משתמש ידידותי ותתמוך בהמלצות וחיפוש מסעדות. המערכת תעוצב כמערכת מבוזרת ותתבסס על תשתיות Flask, עם דגש על תחזוקה ושדרוגים לאורך זמן.
הפרויקט מתמקד בפיתוח מערכת מידע לניהול הזמנות אוכל הכוללת את המרכיבים הבאים:
מנגנון ניהול זהויות: המערכת תכלול שלושה סוגי משתמשים - מנהל, מתפעל ולקוח, כאשר כל משתמש יתחיל את פעילותו על ידי התחברות (Login) עם שם משתמש וסיסמא.
מסך ראשי עם תפריט מותאם: כל משתמש יקבל מסך ראשי עם תפריט המציג את האופציות הרלוונטיות לפעילותו במערכת:
מנהל: יוכל להזין פרטי מנות חדשות.
מתפעל: יוכל לצפות בהזמנות פתוחות ולסגור אותן.
לקוח: יוכל לבצע הזמנות, להזין חוות דעת, לצרף צילומים ולתת ציונים.
ניהול המלצות וחיפוש מסעדות: הלקוח יוכל לחפש מסעדות ולנהל את הזמנותיו בצורה נוחה ואינטואיטיבית.
הפרויקט ישים דגש על מודולריות, נוחות תחזוקה ובקרת תצורה במטרה להבטיח מחזור חיים ארוך ותחזוקה מהירה עם מינימום אי הבנות.
**

סוגי משתמשים-** במערכת יש שלושה סוגי משתמשים, שכל אחד מהם יכול לבצע פעולות שונות בהתאם לתפקידו:
מנהל- 
הזנת פרטי מנות חדשות.
ניהול כלל המערכת והמשתמשים.
ניהול המלצות וחיפוש מסעדות.
מתפעל- 
צפייה בהזמנות פתוחות.
סגירת הזמנות לאחר ביצוען.
לקוח- 
ביצוע הזמנות.
הזנת חוות דעת, צילומים וציונים.
תהליכים- 
עבור המנהל:
הזנת פרטי מנות:
התחברות למערכת.
מעבר למסך ניהול מנות.
הזנת פרטי המנה ושמירתם במערכת.
עבור המתפעל:
צפייה בהזמנות פתוחות:
התחברות למערכת.
מעבר למסך ניהול הזמנות.
צפייה ברשימת ההזמנות הפתוחות.
סגירת הזמנות:
בחירת הזמנה פתוחה.
סימון הזמנה כסגורה.
עבור הלקוח:
ביצוע הזמנה:
התחברות למערכת.
מעבר לתפריט המנות.
בחירת מנות והוספה לסל הקניות.
ביצוע תהליך ההזמנה.
הזנת חוות דעת:
התחברות למערכת.
מעבר למסך הזמנות שבוצעו.
בחירת הזמנה והזנת חוות דעת, צילומים וציונים.
נתונים מנוהלים
נתוני משתמשים:
שם משתמש, סיסמא, תפקיד (מנהל, מתפעל, לקוח).
נתוני מנות:
שם מנה, תיאור, מחיר, תמונה.
נתוני הזמנות:
מזהה הזמנה, מזהה משתמש, פרטי המנות שהוזמנו, תאריך ושעה, סטטוס הזמנה (פתוחה/סגורה).
נתוני חוות דעת:
מזהה משתמש, מזהה מנה, דירוג, טקסט חוות דעת, תמונה.
ארכיטקטורה כוללת
המערכת תתבסס על ארכיטקטורה מבוזרת הכוללת שלוש שכבות (TIERS):
שכבת האינטראקציה עם המשתמשים (Frontend):
מבוססת על HTML/CSS/JS.
שימוש בתבניות Jinja ליצירת דפים דינמיים.
ממשק משתמש ידידותי המותאם לסוגי המשתמשים השונים.
שכבת שרת האפליקציה (Backend):
מבוססת על Flask.
ארגון קוד בתבנית MVC (Model-View-Controller).
יישום לוגיקת העסקים של המערכת.
שכבת שרת הנתונים (Database):
מבוססת על SQLite.
ניהול ואחסון כל הנתונים של המערכת.
שימוש ב-SQL ישיר לניהול הנתונים.
תהליך הזרימה של המידע:
קליטת נתונים:
המשתמש מזין נתונים (למשל, הזמנת אוכל, חוות דעת) דרך ה-Frontend.
עיבוד נתונים:
הנתונים מועברים ל-Backend לעיבוד ואימות.
עיבוד הנתונים מבוצע ב-Flask לפי הלוגיקה המוגדרת.
אחסון נתונים:
הנתונים נשמרים ב-Database באמצעות SQL ישיר.
נתוני הזמנות, מנות, משתמשים, חוות דעת וכו'.
שליפה והצגה של נתונים:
הנתונים נשאבים מה-Database ומעובדים ב-Backend.
הנתונים מוצגים למשתמש ב-Frontend באמצעות תבניות Jinja.
תחזוקה וניהול:
מערכת ניהול גרסאות (כגון GitHub) לניהול הקוד והגרסאות.
חלוקה נכונה של המערכת לרכיביה (מודולציה) להקל על תחזוקה ושדרוגים.
ארכיטקטורה זו מבטיחה מערכת מודולרית, קלה לתחזוקה וניתנת להרחבה, המספקת חווית משתמש טובה וניהול יעיל של המשאבים הדרושים לביצוע המשימות.







