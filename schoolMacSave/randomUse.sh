MAINFILE=XXXXXX ## replace with the FIRST (RIGHT?) part of the directory
EXEFILE=YYYYYY  ## REPLACE WITH THE ABOVE LINE VALUE MINUS ".c"
INPUT_NAME=input-pos
NEGINPUT_NAME=input-neg
OUTPUT_NAME=output-pos
NEGOUTPUT_NAME=output-neg
MY_NAME=my_output
MY_PATH="`dirname \"$0\"`"
rm -R $MY_NAME* &>/dev/null
run_test()
{
  test_case="$1"
if ! $MY_PATH/$EXEFILE < $MY_PATH/$test_case | sed -e '/^$/d' -e 's/^[ \t]*//' > $MY_PATH/$MY_NAME$test_case; then
  exit 2
else
	if diff -b --brief $MY_PATH/$MY_NAME$test_case $2; then
echo "PASS"
exit 0
	else
echo "FAIL"
exit 1
fi
    fi
}
case $1 in
#p1) run_test "$INPUT_NAME"1 "$OUTPUT_NAME"1 ;;
#n1) run_test "$NEGINPUT_NAME"1 "$NEGOUTPUT_NAME"1 ;;
ZZZZZZ
# THERE SHOULD BE THESE FOR HOWEVER MANY ITEMS ARE IN THE TESTS_LIST FILE (MAKE THAT FILE FIRST)

esac
 exit 1
