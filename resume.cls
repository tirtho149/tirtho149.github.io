\ProvidesClass{resume}[2010/07/10 v0.9 Resume class]
\LoadClassWithOptions{article}

\usepackage{array}
\usepackage{ifthen}

\pagestyle{empty}

\def \name#1{\def\@name{#1}}
\def \@name {}

\def \nameskip{\kern 0.25in}
\def \sectionskip{\kern 0.1in}

\newcommand{\printname}{
  \begingroup
    \hfil{\namesize\bf \@name}\hfil
    \nameskip\break
  \endgroup
}

\newcommand{\resheading}[1]{
  {\large \parbox{6.5in}{
    \textbf{#1} \vphantom{p\^{E_p}}
  }}
}

\newcommand{\ressubheading}[4]{
  \begin{tabular*}{6.5in}{l@{\extracolsep{\fill}}r}
    \textbf{#1} & #2 \\
    \textit{#3} & \textit{#4} \\
  \end{tabular*}\vspace{-6pt}
}


\newcommand{\resSection}[1]{
  \sectionskip
  \textbf{#1}
  \sectionskip
  \hrule
  \begin{list}{}{}
  \item[]
}

\let\resEndSection\endlist

\newcommand{\namesize}{\huge}
\newcommand{\addressskip}{\smallskip}
\newcommand{\sectionlineskip}{\medskip}
\newcommand{\rsectionlineskip}{\medskip}
\newcommand{\rSubsectionlineskip}{\smallskip}

\newenvironment{rSection}[1]{
  \sectionskip
  \textbf{\large#1}
  \sectionskip
  \hrule
  \begin{list}{}{\leftmargin=0pt}
  \item[]
}{
  \end{list}
}

\newenvironment{rSubsection}[4]{
  \textbf{#1} \hfill #2 \\
  \textit{#3} \hfill \textit{#4}
  \begin{list}{$\bullet$}{\leftmargin=1em}
  \itemsep -0.5em \vspace{-0.5em}
}{
  \end{list}
  \vspace{0.5em}
}
