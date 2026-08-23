-- ============================================================================
-- PRESS BLITZ TEST — 50 contacts, ~30 seconds
-- Run with: osascript press_blitz_test.applescript
-- After test passes, run press_blitz.applescript for full 1,076
-- ============================================================================

property totalCreated : 0
property totalFailed : 0
property logFile : "/Users/nicholas/clawd/PASSPORT_LAUNCH_13JUN/press_send.log"

on logMsg(msg)
    set theFile to open for access logFile with write permission
    write ((current date) as string) & " | " & msg & return to theFile as string
    close access theFile
end logMsg

on createDraft(theEmail, theFirst, theOutlet, theBeat)
    try
        set theSubject to "[TEST] Open source — the missing A2A primitive, 49 days before the EU cliff"
        set theBody to "Hi " & theFirst & "," & return & return & "This is a test of the MEOK press blitz. Your outlet: " & theOutlet & ". Your beat: " & theBeat & "." & return & return & "If this looks right, the full 1,076 send will run next."
        set newMessage to make new outgoing message with properties {subject:theSubject, content:theBody}
        tell newMessage
            make new to recipient at end of to recipients with properties {address:theEmail}
            set visible to false
        end tell
        set totalCreated to totalCreated + 1
        logMsg ("OK  | " & theEmail & " | " & theFirst & " | " & theOutlet)
    on error errMsg
        set totalFailed to totalFailed + 1
        logMsg ("ERR | " & theEmail & " | " & errMsg)
    end try
end createDraft

on run
    logMsg ("=== PRESS BLITZ TEST (50 contacts) START ===")

    set theContacts to {
        {"edmcfbasupaffocfbasu@forces.gc.ca", "there", "3rd Canadian Division Support Base Edmonton", "general"},
        {"tips@404media.co", "there", "404 Media", "general"},
        {"dnd.gta.4di.publicaffairs-affairespublique.mdn@forces.gc.ca", "there", "4th Canadian Division Headquarters", "general"},
        {"tips@9to5google.com", "there", "9to5Google", "general"},
        {"tips@9to5mac.com", "there", "9to5Mac", "general"},
        {"compliance@a16z.com", "there", "a16z Podcast", "general"},
        {"news.tips@abc.com", "there", "ABC News", "general"},
        {"netaudr@abc.com", "there", "ABC News", "general"},
        {"jonathan.m.newman@abc.com", "there", "ABC News", "general"},
        {"tara.r.gimbel@abc.com", "there", "ABC News", "general"},
        {"newstips@abc.net.au", "there", "ABC News", "general"},
        {"contact@afp.com", "there", "Agence France-Presse", "general"},
        {"contact@aifund.ai", "there", "AI Fund", "general"},
        {"contact@ainowinstitute.org", "there", "AI Now Institute", "general"},
        {"press@ainowinstitute.org", "there", "AI Now Institute", "general"},
        {"press@turing.ac.uk", "there", "Alan Turing Institute", "general"},
        {"info@turing.ac.uk", "there", "Alan Turing Institute", "general"},
        {"digitaltwins@turing.ac.uk", "there", "Alan Turing Institute", "general"},
        {"fdennehy@turing.ac.uk", "there", "Alan Turing Institute", "general"},
        {"mbailey@turing.ac.uk", "there", "Alan Turing Institute", "general"},
        {"interestgroups@turing.ac.uk", "there", "Alan Turing Institute", "general"},
        {"fakset@aaf.mil.al", "there", "Albanian Armed Forces", "general"},
        {"tips@androidcentral.com", "there", "Android Central", "general"},
        {"segr.dirge@ansa.it", "there", "ANSA", "general"},
        {"seg.dirgio@ansa.it", "there", "ANSA", "general"},
        {"commerciale@ansa.it", "there", "ANSA", "general"},
        {"amministrazione@ansa.it", "there", "ANSA", "general"},
        {"cv@ansa.it", "there", "ANSA", "general"},
        {"rcc@ansa.it", "there", "ANSA", "general"},
        {"cronache@ansa.it", "there", "ANSA", "general"},
        {"cultura@ansa.it", "there", "ANSA", "general"},
        {"economia@ansa.it", "there", "ANSA", "general"},
        {"esteri@ansa.it", "there", "ANSA", "general"},
        {"immagini@ansa.it", "there", "ANSA", "general"},
        {"politica@ansa.it", "there", "ANSA", "general"},
        {"redazione.specializzati@ansa.it", "there", "ANSA", "general"},
        {"sport@ansa.it", "there", "ANSA", "general"},
        {"internet@ansa.it", "there", "ANSA", "general"},
        {"dario@anthropic.com", "there", "Anthropic", "general"},
        {"press@arstechnica.com", "there", "Ars Technica", "general"},
        {"tellus@arstechnica.com", "there", "Ars Technica", "general"},
        {"arstechnica@cndservice.com", "there", "Ars Technica", "general"},
        {"mediarelations@ap.org", "there", "Associated Press", "general"},
        {"info@ap.org", "there", "Associated Press", "general"},
        {"leaston@ap.org", "there", "Associated Press", "general"},
        {"pmaks@ap.org", "there", "Associated Press", "general"},
        {"nmeir@ap.org", "there", "Associated Press", "general"},
        {"info@atlanticcouncil.org", "there", "Atlantic Council", "general"},
        {"tips@axios.com", "there", "Axios", "general"},
        {"newswatch@bbc.co.uk", "there", "BBC", "general"},
    ""}

    logMsg ("Loaded " & (count of theContacts) & " test contacts")
    repeat with aContact in theContacts
        if (class of aContact) is string then exit repeat
        set {theEmail, theFirst, theOutlet, theBeat} to aContact
        my createDraft(theEmail, theFirst, theOutlet, theBeat)
    end repeat

    logMsg ("=== TEST COMPLETE: created=" & totalCreated & " failed=" & totalFailed & " ===")
    display dialog ("Test complete" & return & return & "Created: " & totalCreated & return & "Failed: " & totalFailed & return & return & "Open Mail.app Drafts to review the 50 test drafts.") buttons {"OK"} default button "OK"
end run