

def clean_ethnic_file(df):
    df['Ethnic'] = df['Full Name'].apply(categorize_ethnic)
    return rename_column(df)

def categorize_ethnic(name):
   ethnicity_mapping = {
    'Chinese': {'lee', 'tan', 'lim', 'wong', 'ng', 'yee', 'chin', 'ling', 'chan', 'chong', 'wei', 'hui',
                'yong', 'siew', 'chee', 'lai', 'leong', 'ong', 'hong', 'wai', 'mei', 'yap', 'kok', 'low',
                'goh', 'ying', 'chai', 'cheng', 'fong', 'yi', 'li', 'yen', 'liew', 'kim', 'ting', 'wan',
                'chew', 'chen', 'seng', 'ho', 'ching', 'kong', 'jia', 'pei', 'loh', 'lau', 'yin', 'choo',
                'eng', 'heng', 'boon', 'mun', 'wee', 'wen', 'ooi', 'soon', 'tee', 'lin', 'chua', 'min',
                'sim', 'gan', 'ang', 'poh', 'foo', 'yan', 'see', 'ming', 'peng','teh', 'teoh', 'yu', 'yoke',
                'tang', 'kee', 'sin','chang','teng','soo','xin','meng', 'ai', 'lian', 'bee', 'chia','jun',
                'kuan', 'ping','chun','khoo', 'kah', 'qi', 'yew', 'koh', 'ah', 'weng', 'leng', 'choon', 'wah',
                'tong', 'shin', 'lay', 'kai', 'foong', 'yang', 'cheah', 'tai', 'swee', 'han', 'hooi', 'yeoh',
                'jing', 'fei', 'san', 'loo', 'ee', 'toh','sze', 'tay', 'sook', 'lam', 'su', 'pang', 'shu',
                'hoon', 'jin', 'zhi', 'kian', 'may', 'hoo', 'liang', 'khor', 'huat', 'hock', 'beng', 'xuan',
                'yun', 'guan', 'keong', 'chung','choong', 'sing', 'woon', 'chiew', 'keng', 'mee', 'jie', 'siang',
                'chooi', 'ann', 'saw', 'chuan', 'teo', 'chow', 'soh', 'sam', 'hua', 'nee', 'seow', 'kit', 'pui',
                'kang', 'yoong', 'lan', 'shi', 'yuen', 'hwa', 'huey', 'thong', 'tze', 'keat', 'voon', 'kin', 'en',
                'teck', 'man', 'hoong', 'wang', 'kwan', 'sharon', 'yip', 'sheng', 'fook', 'how', 'chu', 'yuan',
                'phang', 'chuah', 'shen', 'chi', 'siong', 'kam', 'sia', 'kean', 'zi', 'yeong', 'shan', 'yeo', 'loong', 'loke', 'ni', 'oon', 'koon', 'yoon', 'kar', 'woo', 'khoon', 'theng', 'qian', 'er',
                'hwee', 'zhang', 'fang', 'lew', 'fun', 'irene', 'tham', 'yau', 'tian', 'guat', 'sun', 'law', 'ken',
                'xiao', 'moi', 'fatt', 'yung', 'hon', 'hew', 'mooi', 'xian', 'liu', 'lye', 'zheng', 'koo', 'tey',
                'seong', 'beh', 'siow', 'hin', 'shing', 'pin', 'zhe', 'chui', 'rui', 'onn', 'kuen', 'long', 'khong',
                'wu', 'wing', 'fung', 'feng', 'kien', 'yean', 'yeow', 'khai', 'zhen', 'pooi', 'jong', 'jian', 'haw',
                'joo', 'tiong', 'choy', 'geok', 'hao','liaw', 'jen', 'aw', 'hung', 'hee', 'jenny', 'thiam', 'lean',
                'qing', 'jason', 'yik', 'ye', 'xing', 'hang', 'mui', 'neo', 'kho', 'huang', 'alex', 'hoe', 'na', 'kiew',
                'alice', 'amy', 'looi', 'siaw', 'sue', 'sai', 'bong', 'poon', 'song', 'shun', 'nguyen', 'fui', 'vivian',
                'chuen', 'ha', 'lu', 'chea', 'pey', 'le', 'suan', 'teong', 'you', 'sen','hau', 'khaw', 'carmen', 'ing',
                'moy', 'yeng', 'sok', 'ivy','ewe', 'kiang', 'joseph', 'qin', 'king','too', 'boo', 'bing', 'chian',
                'yue', 'tuck', 'ngan', 'sow', 'sang', 'sum', 'che', 'oh', 'tin', 'kum', 'al', 'tung', 'joanne', 'oo',
                'pheng', 'yeap', 'agnes', 'koay', 'yao', 'jane', 'kwong', 'har', 'pek', 'michelle', 'soong', 'phooi',
                'chieng', 'raymond', 'hiew', 'eunice', 'cheang', 'mah', 'mong', 'kun', 'mary', 'leow', 'lih', 'kua',
                'nicole', 'kaiming', 'liau', 'cheong','poonsiewlee'},

    'Malay': {'ahmad','abdul','abdullah','zurina', 'mohd', 'bin', 'binti', 'muhammad', 'mohamed', 'mohamad',
              'siti','nurul', 'nor', 'mohammad', 'ismail', 'md', 'ali', 'syed', 'noor', 'ibrahim', 'abd',
              'hamba', 'allah', 'yusof', 'rahman', 'rahim', 'azhar', 'khan', 'azmi', 'othman', 'zainal', 'sulaiman',
              'mohammed', 'hashim', 'fatin', 'hassan', 'nik', 'hussin', 'sharifah', 'mat', 'razali', 'faizal', 'aiman',
              'khairul', 'firdaus', 'arif', 'warsi','manaf', 'aini', 'nur','muhamad', 'bakar', 'nadia','farah','omar','abu',
              'farahzira','zakaria','norkiah','mahmud','nordin','ahmed','hasan','aleya','aziz','aina','adam','Sharmila',
              'nabihah','arifin','yahya','ishak','anis','meor','liza','alia','isa','norliana','nadzirah','noordin','shahmin','rashid','aishah',
              'arshad','ariff','izzat','ramli','diana','matin','akbar','halim','harun','aizat','jamal','amira','idris','tengkushahz','shamsuddin',
              'nurhasikin','syahiratul','norhairul','baharudin','zulkiffli','nooraihan','zainuddin','nursafira','kamardin', 'amalina', 'zulkifli', 'hamid','hamzah'
              'noratikah','syamimi, latif','ungku','aminah','mohsin'},

    'Indian': {'a/l', 'a/p','rajandran', 'subramaniam','kumar','krishnan', 'devi', 'raja', 'singh', 'muniandy', 'raman', 'nair', 'rao',
               'naidu','krishna', 'ramasamy','esvini', 'panirchellvum', 'hareeshkumar', 'kalaiselvan', 'sugitha', 'anbalagan',
               'tamilselvi', 'rajendran', 'shaamini','chandrasekharan', 'annamalai','kuppusamy','vathi', 'punitha', 'sinawadoo',
                'ratha', 'sri','balakrishnan', 'gunasegaran', 'selvam', 'ravichandran', 'manogaran', 'selvaraj',
                'prakash', 'moorthy', 'mohan', 'ravi', 'supramaniam','paramasivam', 'ravindran', 'kandasamy',
               'selvaraju', 'mahendran','shanmugam', 'arumugam','ganesan','priya','rajan','rajah','pannirselvan'
                'govindasamy','sivalingham','letchmanan','ashwinath','muthusamy','sangeetha','ponnusamy','sarasvati',
               'piraveen','chandran','jethwani','gayatrri','nadaraja','vijayan','suppiah','murugan','ramesh','vijaya',
               'sharma','malani','susila','pillai','chitra','balan','rhenu','surin','teeba','kalai','rajes','para','sami',
               'balasubramaniam','letchumanan','herrentiran','vigneswaran','subhashini','palaniandy','sarasvathy','jaganathan',
               'ganditasan','manigandan','selvakumar','selvarani','pothuraju','manimaran','nadarajah','karuppiah','doraisamy',
               'marimuthu','manoharan','rajeswari','mariappan','nadarajan','sukumaran','saravanan','ravendran','sangaram','letchumi',
               'amertham','munusamy','sundaram','suganthi','murugiah','vishnu','ravin','muthu','rajoo','vevak','samayamunisusilla','chandrasegaran',
               'shanmugaphria','krishnamurthy','limthiangseng','somasundharam','tavaneisvaran','sahulhamithu','pannirselvan','govindarajoo','kalaichelvan',
               'vaithalingam','kumaresvaran','parameswaran','singaraveloo','suthenthiran','muthukrishna','kaliaperumal','geethaanjali','navaneetham',
               'thinagarash','sandanasamy','gnapragasan','subramanian','govindasamy','palaniappan','sivananthan','kunasagaran','rajendaran','thevarajoo','jakathesan',
               'arunawathi','ravindaran','kaneskumar','jeganathan','gopinathan','chowdhury','yantimala','shanmugom','batumalay','vasudevan','narayanan','periasamy',
               'yaashdave','arulmozhi','sagadevan','jeyamaran','rengasamy','ilavarasi','thiriidev','prashanth','rajkumar','karthiga','vasanthi','darmaraju'},

    'Others': {'john', 'james', 'emily', 'family', 'edward', 'grace', 'rachel', 'david', 'audrey', 'gomes', 'florance', 'nyihin',
               'elisa', 'christy', 'christ', 'elango', 'minjae','hera', 'pauline', 'jon', 'michael','thida','wendy',
               'phina','ambrose','haller','martin','samuel','stacy','nikko','harry','hema','anna','devy','mia','christopher',
               'bernadette','alexandra','josephine','emmanuel','priscila','jonathan','benedict','jessica','anthony','jasmine','francis','kanmani',
               'rebecca','charles','ramday','angela','judith','nathan','alicia','thomas','jimmy','mogana','annie','reddy','jacob','brown','wattanagitiphat',
               'nageiswery','jessamine','chrizelda','frederick','sherlynee','jessindra','nattawin','swatheka','florence','jennifer','wazooski', 'fernandez'},
   } 

   name_words = name.lower()
   for category, words in ethnicity_mapping.items():
      for word in name_words.split():
         if word in words:
             return category
   return ''

# Check progress and distinct in ethnics
def check_progress(df):
   blank_rows = len(df[df['Ethnic'].isnull() | df['Ethnic'].eq('')])
   non_blank_rows = len(df[~df['Ethnic'].isnull() & ~df['Ethnic'].eq('')])
   total_rows = df.shape[0]
   distinct_values = df['Ethnic'].unique()
   
   print("Progress...")
   print(f"Total rows: {total_rows}")
   print(f"Blank rows: {blank_rows}")
   print(f"Non-blank rows: {non_blank_rows}")
   
   print("Distinct Item in Ethnic column: ")
   print(distinct_values)

   return df

def rename_column(df):
    df.rename(columns = {'Ethnic' : 'MCO_Ethnic__c'}, inplace=True)

    return df