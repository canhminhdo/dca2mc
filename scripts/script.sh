cat ../lib/prelude.maude | \
    grep -E '^[\t ]*(fmod|mod|fth|view)' | \
    sed 's/ is//' | \
    sed 's/ from.*//' | \
    sed 's/{.*//' | \
    sed "s/view /v('/" | \
    sed -E "s/(fmod|mod|fth) /m('/" | \
    sed 's/$/)/'

cat ../full-maude-lite.maude | \
    grep -E '^(fmod|mod|fth|view)' | \
    sed 's/ is//' | \
    sed 's/ from.*//' | \
    sed 's/{.*//' | \
    sed "s/view /v('/" | \
    sed -E "s/(fmod|mod|fth) /m('/" | \
    sed 's/$/)/'

cat ../utils.maude | \
    grep -E '^(fmod|mod|fth|view)' | \
    sed 's/ is//' | \
    sed 's/ from.*//' | \
    sed 's/{.*//' | \
    sed "s/view /v('/" | \
    sed -E "s/(fmod|mod|fth) /m('/" | \
    sed 's/$/)/'

cat ../database.maude | \
    grep -E '^(fmod|mod|fth|view)' | \
    sed 's/ is//' | \
    sed 's/ from.*//' | \
    sed 's/{.*//' | \
    sed "s/view /v('/" | \
    sed -E "s/(fmod|mod|fth) /m('/" | \
    sed 's/$/)/'

cat ../checker.maude | \
    grep -E '^(fmod|mod|fth|view)' | \
    sed 's/ is//' | \
    sed 's/ from.*//' | \
    sed 's/{.*//' | \
    sed "s/view /v('/" | \
    sed -E "s/(fmod|mod|fth) /m('/" | \
    sed 's/$/)/'