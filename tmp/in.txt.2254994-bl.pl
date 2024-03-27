#!/usr/bin/env perl
$host = shift;
$instance = shift;
$arg = shift;

#### random sleep, rand() can be a fraction of second
select(undef,undef,undef,rand());

if ($arg) {
  @ids = split(/,/, $arg);
}
else {
  while(1) {
    if (opendir(DDIR, "tmp/in.txt-seq")) { 
      @ids = grep {/^\d+$/} readdir(DDIR);
      last;
    }
    else {
      sleep(1);
    }
  }
}

foreach $id (@ids) {

  next unless (-e "tmp/in.txt-seq/$id");
  next if (-e "tmp/in.txt-seq/$id.lock");
  $cmd = `touch tmp/in.txt-seq/$id.lock`;

  if (50) {
    $cmd = `blastp -outfmt 6 -db ./tmp/in.txt.2254994 -seg yes -evalue 0.000001 -max_target_seqs 100000 -num_threads 4 -query tmp/in.txt-seq/$id -out tmp/in.txt-bl/$id`;
    $cmd =                         `./cdhit/psi-cd-hit/psi-cd-hit.pl -J parse_blout_multi tmp/in.txt-bl/$id -c 0.3 -ce 1e-6 -aS 0 -aL 0 -G 0 -prog blastp -bs 0 >> tmp/in.txt-blm/$host.$instance`;
  }
  elsif (1) {
    $cmd = `blastp -outfmt 6 -db ./tmp/in.txt.2254994 -seg yes -evalue 0.000001 -max_target_seqs 100000 -num_threads 4 -query tmp/in.txt-seq/$id | ./cdhit/psi-cd-hit/psi-cd-hit.pl -J parse_blout tmp/in.txt-bl/$id -c 0.3 -ce 1e-6 -aS 0 -aL 0 -G 0 -prog blastp -bs 1`;
  }
  else {
    $cmd = `blastp -outfmt 6 -db ./tmp/in.txt.2254994 -seg yes -evalue 0.000001 -max_target_seqs 100000 -num_threads 4 -query tmp/in.txt-seq/$id -out tmp/in.txt-bl/$id`;
    $cmd =                         `./cdhit/psi-cd-hit/psi-cd-hit.pl -J parse_blout tmp/in.txt-bl/$id -c 0.3 -ce 1e-6 -aS 0 -aL 0 -G 0 -prog blastp -bs 0`;
  }
  $cmd = `rm -f  tmp/in.txt-seq/$id`;
  $cmd = `rm -f  tmp/in.txt-seq/$id.lock`;
}

($tu, $ts, $cu, $cs) = times();
$tt = $tu + $ts + $cu + $cs;
$cmd = `echo $tt >> tmp/in.txt-seq/host.$host.$instance.cpu`;

